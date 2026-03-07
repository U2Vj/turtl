import os
import time
import asyncio
import logging
import requests
from proxmoxer import ProxmoxAPI
from django.db import transaction, IntegrityError
from django.utils import timezone
from dotenv import load_dotenv
from .utils import AdvisoryLock, slugify, format_ip
from .models import LabEnvironment, TaskVMConfiguration, Network, VirtualMachine

"""
To set up Proxmox VE place a .env File in the root of the project and fill in the following variables:
- PROXMOX_HOST
- PROXMOX_USER
- PROXMOX_PASSWORD
"""
load_dotenv()
logger = logging.getLogger(__name__)


class ProxmoxManager:
    # Constants
    LOCK_TIMEOUT = 120
    POLL_INTERVAL = 2
    LOCK_ACQUIRE_TIMEOUT = 30
    def __init__(self):
        try:
            host = os.environ.get('PROXMOX_HOST')
            user = os.environ.get('PROXMOX_USER')
            password = os.environ.get('PROXMOX_PASSWORD')
            verify_param = self._get_verify_param()

            # Initialize Proxmox API connection
            self.proxmox = ProxmoxAPI(
                host=host,
                user=user,
                password=password,
                verify_ssl=verify_param,
            )
            # Add attribute to store auth cookie for VNC WebSocket auth
            self.auth_cookie = None
        except Exception:
            logger.exception("Failed to connect to Proxmox API")
            raise

    def _authenticate(self):
        """
        Ensure we are authenticated and have a valid auth cookie.
        If not authenticated, perform a login request and store the cookie.
        """
        if self.auth_cookie:
            return
        verify_param = self._get_verify_param()

        try:
            logger.debug("Authenticating with Proxmox")
            login_response = requests.post(
                f"https://{os.environ.get('PROXMOX_HOST')}/api2/json/access/ticket",
                data={
                    "username": os.environ.get('PROXMOX_USER'),
                    "password": os.environ.get('PROXMOX_PASSWORD')
                },
                verify=verify_param
            )
            login_response.raise_for_status()
            login_data = login_response.json()["data"]

            self.auth_cookie = login_data["ticket"]
            logger.debug("Successfully authenticated with Proxmox")
        except requests.exceptions.RequestException:
            logger.exception("Proxmox authentication failed")
            raise

    def get_auth_cookie(self):
        """
        Returns the stored authentication cookie, authenticating if necessary.
        """
        if not self.auth_cookie:
            self._authenticate()
        return self.auth_cookie

    # Helper functions
    def _get_verify_param(self):
        ca_path = os.environ.get('PROXMOX_CA_PATH')
        verify_env = os.environ.get('PROXMOX_VERIFY_SSL', 'true').strip().lower()

        if verify_env in ('false', '0'):
            return False
        elif ca_path:
            return ca_path
        else:
            return False

    def get_node(self):
        """
        Get a available Proxmox node
        TODO: Add proper load balancing for multiple nodes
        """
        try:
            nodes = self.proxmox.nodes.get()
            for node in nodes:
                if node['status'] == 'online':
                    logger.debug("Found online Proxmox node=%s", node['node'])
                    return node['node']
            raise Exception("No available nodes in cluster")
        except Exception:
            logger.exception("Error finding suitable Proxmox node")
            raise
        
    def create_lab_environment(self, user, task):
        """
        Create a new lab environment for a user and task.
        1. Create network
        2. Create VMs from the task configuration
        """

        # create lock on user-task to prevent attempted creation of duplicate environments
        lock_name = f"lab_env_{user.id}_{task.id}"

        with AdvisoryLock(lock_name, timeout_seconds=self.LOCK_ACQUIRE_TIMEOUT) as acquired:
            if not acquired:
                raise TimeoutError(f"Could not acquire lock for lab environment creation (user: {user.id}, task: {task.id})")

            try:
                #Check if environment already exists
                existing_env = LabEnvironment.objects.filter(user=user, task=task).first()
                if existing_env:
                    logger.info(
                        "Lab environment already exists for user_id=%s task_id=%s",
                        user.id,
                        task.id,
                    )
                    return existing_env
                
                task_config = TaskVMConfiguration.objects.filter(task=task).first()
                if not task_config:
                    raise ValueError(f"No VM configuration found for task: {task.title}")
                
                with transaction.atomic():
                    # 1. Create network
                    network = self.provision_network(user, task, task_config)

                    # 2. Create the lab environment record
                    lab_env = LabEnvironment.objects.create(
                        user=user,
                        task=task,
                        network=network
                    )
                    
                    # 3. Create all VMs for env
                    for vm_template_config in task_config.vm_templates.all():
                        self.provision_vm(lab_env, vm_template_config, network, user, task)

                    # 4. Update lab_env status
                    lab_env.status = 'active'
                    lab_env.last_seen_at = timezone.now()
                    lab_env.stopped_at = None
                    lab_env.save()

                    return lab_env

            except Exception:
                logger.exception(
                    "Error creating lab environment for task_id=%s user_id=%s",
                    task.id,
                    user.id,
                )
                self.cleanup_orphans()
                raise
    
    def provision_network(self, user, task, task_config):
        """
        Creates a network in Proxmox based on the network template from task config
        """
        network_template = task_config.network_template
        if not network_template:
            raise ValueError(f"No network template defined for task: {task.title}")
        
        # Lock on network creation process
        lock_name = "proxmox_bridge_creation"

        with AdvisoryLock(lock_name, timeout_seconds=self.LOCK_ACQUIRE_TIMEOUT) as acquired:
            if not acquired:
                raise TimeoutError("Could not acquire lock for bridge allocation")
            
            max_retries = 10
            for attempt in range(max_retries):
                try:
                    with transaction.atomic():
                        # 1. Find next available Bridge ID
                        highest_vlan = Network.objects.select_for_update().filter(vlan_id__isnull=False).order_by('-vlan_id').first()

                        bridge_id = highest_vlan.vlan_id + 1 if highest_vlan else 100
                        bridge_name = f"vmbr{bridge_id}"
                        network_name = f"{slugify(task.title)}-{slugify(user.username)}-net"
                        node = self.get_node()

                        # 2. Create network in database
                        network = Network.objects.create(
                            name=network_name,
                            subnet=network_template.subnet,
                            vlan_id=bridge_id,
                            template=network_template,
                            user=user,
                            task=task
                        )

                        try:
                            # 3. Create bridge in Proxmox
                            self.create_bridge(
                                node=node,
                                bridge=bridge_name,
                                cidr=network_template.subnet
                            )
                        except Exception:
                            logger.exception(
                                "Error creating bridge in Proxmox bridge=%s task_id=%s user_id=%s",
                                bridge_name,
                                task.id,
                                user.id,
                            )
                            raise

                        return network
                except IntegrityError as e:
                    if 'vlan_id' in str(e) and attempt < max_retries - 1:
                        logger.warning(
                            "VLAN ID collision vlan_id=%s, retrying attempt=%s/%s",
                            bridge_id,
                            attempt + 1,
                            max_retries,
                        )
                        # Short delay before retry to allow other transactions to complete
                        time.sleep(0.3)
                        continue
                    else:
                        logger.exception(
                            "Failed to allocate unique VLAN ID after retries=%s",
                            max_retries,
                        )
                        raise
    
    def create_bridge(self, node, bridge, cidr, gateway=None, autostart=True):
        """
        Creates a new Linux bridge in Proxmox and activates it directly.
        """
        try:
            existing = self.proxmox.nodes(node).network.get()
            if any(net.get('iface') == bridge for net in existing):
                logger.info("Bridge already exists, skipping create bridge=%s node=%s", bridge, node)
                try:
                    self.proxmox.nodes(node).network(bridge).up.post()
                except Exception:
                    logger.warning(
                        "Failed to bring up existing bridge bridge=%s node=%s",
                        bridge,
                        node,
                        exc_info=True,
                    )
                return
        except Exception:
            logger.exception("Error checking existing Proxmox networks node=%s bridge=%s", node, bridge)
            raise

        params = {
            'iface': bridge,
            'type': 'bridge',
            'cidr':cidr,
            'autostart': int(autostart)
        }
        if gateway:
            params['gateway'] = gateway

        try:
            result = self.proxmox.nodes(node).network.post(**params)
            logger.info("Network bridge created bridge=%s node=%s result=%s", bridge, node, result)
            self.proxmox.nodes(node).network.put()
            logger.debug("Network configuration reloaded node=%s", node)
        except Exception:
            logger.exception("Error creating network bridge=%s node=%s", bridge, node)
            raise

    def provision_vm(self, lab_env, vm_template_config, network, user, task):
        """
        Create VM in Proxmox and configure it for network
        """

        # lock for global VM creation
        vm_creation_lock = "proxmox_vm_creation"

        with AdvisoryLock(vm_creation_lock, timeout_seconds=self.LOCK_ACQUIRE_TIMEOUT) as acquired:
            if not acquired:
                raise TimeoutError("Could not acquire lock for VM creation")
            
            try:
                template = vm_template_config.template
                node = self.get_node()
                vmid = self.proxmox.cluster.nextid.get()
                vm_name = f"vm-{slugify(lab_env.task.title)}-{slugify(lab_env.user.username)}-{slugify(template.name)}"
                ip_address = format_ip(vm_template_config.planned_ip_address, network)

                # Clone VM from template
                logger.debug(
                    "Cloning VM from template template_id=%s vm_name=%s vmid=%s",
                    template.template_id,
                    vm_name,
                    vmid,
                )
                self.clone_vm(
                    node=node,
                    template_id=template.template_id,
                    new_id=vmid,
                    new_name=vm_name,
                )

                bridge_name = f"vmbr{network.vlan_id}"

                logger.debug("Configuring VM networking vmid=%s bridge=%s", vmid, bridge_name)
                storage = 'local-lvm'
                ci_user = 'student'
                ci_password = 'student'

                self.configure_vm(
                    node=node,
                    vm_id=vmid,
                    storage=storage,
                    ci_user=ci_user,
                    ci_password=ci_password,
                    bridge=bridge_name,
                    ip_address=ip_address,
                    cpu_cores=template.cpu_cores,
                    memory_mb=template.memory_mb,
                )

                #Add VM to database
                with transaction.atomic():
                    vm = VirtualMachine.objects.create(
                        vmid=vmid,
                        lab_environment=lab_env,
                        template=template,
                        name=vm_name,
                        status='creating',
                        network=network,
                        assigned_ip_address=ip_address.split('/')[0]
                    )

                    #Start the VM
                    logger.debug("Starting VM vmid=%s", vmid)
                    self.proxmox.nodes(node).qemu(vmid).status.start.post()

                    # Update status
                    vm.status = 'running'
                    vm.save()
                
                return vm
            except Exception:
                logger.exception(
                    "Error provisioning VM for task_id=%s user_id=%s env_id=%s",
                    task.id,
                    user.id,
                    lab_env.id,
                )
                raise

    def clone_vm(self, node, template_id, new_id, new_name, linked_clone=True):
        """
        Clones a VM from a template_id as a linked clone
        """
        params = {
            'newid': new_id,
            'name' : new_name,
            'target': node,
            'full': 0 if linked_clone else 1
        }

        try:
            self.proxmox.nodes(node).qemu(template_id).clone.post(**params)
            logger.debug("Clone command sent for vmid=%s from template_id=%s", new_id, template_id)
        except Exception:
            logger.exception(
                "Error cloning template template_id=%s new_id=%s node=%s",
                template_id,
                new_id,
                node,
            )
            raise

        logger.debug("Waiting for lock removal on vmid=%s", new_id)
        self.wait_for_unlock(node, new_id)
        logger.debug("Lock removed from vmid=%s", new_id)

    def wait_for_unlock(self, node, vm_id, timeout=None, interval=None):
        """
        Waits until the VM Lock is removed by Proxmox
        """
        if timeout is None:
            timeout = self.LOCK_TIMEOUT
        if interval is None:
            interval = self.POLL_INTERVAL

        start = time.time()
        while True:
            locks = self.proxmox.nodes(node).qemu(vm_id).status.current.get().get('lock')
            if not locks:
                return
            if time.time() - start > timeout:
                raise TimeoutError(f"Timeout waiting for unlock of VM {vm_id}")
            time.sleep(interval)

    def configure_vm(self, node, vm_id, storage, ci_user, ci_password, bridge, ip_address, cpu_cores, memory_mb):
        """
        Configures the VM via Cloud-init
        """
        try:
            config_params = {
                'ide2': f"{storage}:cloudinit",
                'ciuser': ci_user,
                'net0': f"virtio,bridge={bridge}",
                'ipconfig0': f"ip={ip_address}",
                'cipassword': ci_password,
                'agent': 'enabled=1',
                'boot': 'order=scsi0',
                'cicustom': 'user=local:snippets/user-data.yaml',
                'sockets': 1,
                'cores': int(cpu_cores),
                'memory': int(memory_mb),
            }

            self.proxmox.nodes(node).qemu(vm_id).config.post(**config_params)
            logger.debug("VM options set successfully vmid=%s", vm_id)
        except Exception:
            logger.exception("Error configuring VM vmid=%s node=%s", vm_id, node)
            raise

    def start_environment(self, lab_env):
        """
        Starts all VMs inside a lab environment
        """
        env_operation_lock = f"lab_env_operation_{lab_env.id}"
        with AdvisoryLock(env_operation_lock, timeout_seconds=self.LOCK_ACQUIRE_TIMEOUT) as acquired:
            if not acquired:
                raise TimeoutError(f"Could not acquire lock for starting environment {lab_env.id}")
            
            try:
                lab_env.status = 'starting'
                lab_env.save()
                node = self.get_node()
                with transaction.atomic():
                    for vm in lab_env.virtual_machines.select_for_update().all():
                        if vm.status != 'running':
                            # Start the VM
                            self.proxmox.nodes(node).qemu(vm.vmid).status.start.post()
                            vm.status = 'running'
                            vm.save()
                    # Update lab environment status
                    if lab_env.status != 'active':
                        lab_env.status = 'active'
                        lab_env.stopped_at = None
                        lab_env.last_seen_at = timezone.now()
                        lab_env.save()
                return True
            except Exception:
                logger.exception("Error starting lab environment env_id=%s", lab_env.id)
                return False

    def stop_environment(self, lab_env):
        """
        Stops all VMs inside a lab environment
        """
        env_operation_lock = f"lab_env_operation_{lab_env.id}"
        with AdvisoryLock(env_operation_lock, timeout_seconds=self.LOCK_ACQUIRE_TIMEOUT) as acquired:
            if not acquired:
                raise TimeoutError(f"Could not acquire lock for stopping environment {lab_env.id}")
            
            try:
                lab_env.status = 'stopping'
                lab_env.save()
                node = self.get_node()

                with transaction.atomic():
                    for vm in lab_env.virtual_machines.select_for_update().all():
                        if vm.status == 'running':
                            # Stop the VM
                            self.proxmox.nodes(node).qemu(vm.vmid).status.stop.post()
                            # Update VM status
                            vm.status = 'stopped'
                            vm.save()

                    current_time = timezone.now()
                    update_fields = []

                    if lab_env.status != 'stopped':
                        lab_env.status = 'stopped'
                        update_fields.append('status')

                    if lab_env.stopped_at is None:
                        lab_env.stopped_at = current_time
                        lab_env.last_seen_at = current_time
                        update_fields.extend(['stopped_at', 'last_seen_at'])

                    if update_fields:
                        lab_env.save(update_fields=update_fields)
                return True
            except Exception:
                logger.exception("Error stopping lab environment env_id=%s", lab_env.id)
                if lab_env.status == 'stopping':
                    lab_env.status = 'active'
                    lab_env.save(update_fields=['status'])
                raise

    def cleanup_environment(self, user, task):
        """
        Deletes all VMs and the network of a lab environment for a given user and task. Then deletes the lab environment.
        """

        def _cleanup():
            env_cleanup_lock = f"lab_env_cleanup_{user.id}_{task.id}"

            with AdvisoryLock(env_cleanup_lock, timeout_seconds=self.LOCK_ACQUIRE_TIMEOUT) as acquired:
                if not acquired:
                    logger.warning(
                        "Could not acquire lock for cleanup user_id=%s task_id=%s",
                        user.id,
                        task.id,
                    )
                    return "locked"
                
                try:
                    # Get the lab environment
                    lab_env = LabEnvironment.objects.filter(user=user, task=task).first()
                    if not lab_env:
                        logger.info(
                            "No lab environment found for cleanup user_id=%s task_id=%s",
                            user.id,
                            task.id,
                        )
                        return "not_found"
                    # Mark environment as being cleaned up
                    if lab_env.status != 'cleanup':
                        lab_env.status = 'cleanup'
                        lab_env.save()
                    # Delete all VMs
                    for vm in lab_env.virtual_machines.all():
                        try:
                            node = self.get_node()
                            # Stop the VM
                            try:
                                self.proxmox.nodes(node).qemu(vm.vmid).status.stop.post()
                                # Wait for VM to stop
                                time.sleep(5)
                            except Exception:
                                logger.warning(
                                    "Could not stop VM during cleanup vmid=%s env_id=%s",
                                    vm.vmid,
                                    lab_env.id,
                                    exc_info=True,
                                )
                            self.proxmox.nodes(node).qemu(vm.vmid).delete()
                            # Delete VM from database
                            vm.delete()
                        except Exception:
                            logger.warning(
                                "Could not delete VM during cleanup vmid=%s env_id=%s",
                                vm.vmid,
                                lab_env.id,
                                exc_info=True,
                            )
                    
                    # Delete the network
                    if lab_env.network:
                        try:
                            if lab_env.network.vlan_id:
                                node = self.get_node()
                                bridge_name = f"vmbr{lab_env.network.vlan_id}"
                                
                                # Delete the bridge
                                try:
                                    # Bring down bridge first
                                    self.proxmox.nodes(node).network(bridge_name).delete()
                                    # Apply network changes
                                    self.proxmox.nodes(node).network.put()
                                except Exception:
                                    logger.warning(
                                        "Could not delete bridge during cleanup bridge=%s env_id=%s",
                                        bridge_name,
                                        lab_env.id,
                                        exc_info=True,
                                    )
    
                            # Delete network from database
                            lab_env.network.delete()
                        except Exception:
                            logger.warning(
                                "Error deleting network during cleanup env_id=%s",
                                lab_env.id,
                                exc_info=True,
                            )

                    # Delete lab environment
                    lab_env.delete()
                    return "deleted"
                                
                except Exception:
                    logger.exception(
                        "Error during cleanup for user_id=%s task_id=%s",
                        user.id,
                        task.id,
                    )
                    self.cleanup_orphans()
                    return "failed"

        return _cleanup()
    
    def cleanup_orphans(self):
        """
        Searches for orphan Resources in Proxmox regarding Networks and VMs and deletes them. Maybe run this in a CRON Job later
        """
        with AdvisoryLock("proxmox-cleanup", timeout_seconds=self.LOCK_ACQUIRE_TIMEOUT) as acquired:
            if not acquired:
                return
            
            # check if vm or network creation is ongoing, if yes do not cleanup
            with AdvisoryLock("proxmox_vm_creation", timeout_seconds=self.LOCK_ACQUIRE_TIMEOUT) as vm_lock_acquired, \
             AdvisoryLock("proxmox_bridge_creation", timeout_seconds=self.LOCK_ACQUIRE_TIMEOUT) as net_lock_acquired:

                if not (vm_lock_acquired and net_lock_acquired):
                    return
                cluster_node = self.get_node()
                resources = self.proxmox.cluster.resources.get(type='vm')
                for r in resources:
                    name = r.get('name', '')
                    vmid = int(r.get('vmid'))
                    
                    if not name.startswith("vm-"):
                        continue
                    
                    if not VirtualMachine.objects.filter(vmid=vmid).exists():
                        logger.info("Found orphan VM vmid=%s name=%s, deleting", vmid, name)
                        try:
                            node = r.get('node') or self.get_vm_node(vmid)
                            self.proxmox.nodes(node).qemu(vmid).status.stop.post()
                            time.sleep(5)
                            self.proxmox.nodes(node).qemu(vmid).delete()
                        except Exception:
                            logger.warning("Could not delete orphan VM vmid=%s", vmid, exc_info=True)

                nets = self.proxmox.nodes(cluster_node).network.get()
                for net in nets:
                    iface = net.get('iface')
                    if not iface:
                        continue
                    if not iface.startswith("vmbr"):
                        continue
                    try:
                        vlan_id = int(iface.replace("vmbr", ""))
                    except ValueError:
                        continue
                    if vlan_id < 100:
                        continue

                    if not Network.objects.filter(vlan_id=vlan_id).exists():
                        logger.info("Found orphan bridge iface=%s, deleting", iface)
                        try:
                            self.proxmox.nodes(cluster_node).network(iface).delete()
                            self.proxmox.nodes(cluster_node).network.put()
                        except Exception:
                            logger.warning(
                                "Could not delete orphan bridge iface=%s",
                                iface,
                                exc_info=True,
                            )

    def sync_vm_status(self, lab_env):
        """
        Synchronizes VM status with Proxmox for a lab environment
        """

        try:
            node = self.get_node()

            any_vm = False
            all_running = True
            all_stopped = True

            for vm in lab_env.virtual_machines.all():
                any_vm = True
                try:
                    vm_status = self.proxmox.nodes(node).qemu(vm.vmid).status.current.get().get('status')

                    if vm.status != vm_status:
                        vm.status = vm_status
                        vm.save()

                    if vm_status != 'running':
                        all_running = False
                    if vm_status != 'stopped':
                        all_stopped = False
                except Exception:
                    logger.warning(
                        "Could not sync status for VM vmid=%s env_id=%s",
                        vm.vmid,
                        lab_env.id,
                        exc_info=True,
                    )
                    all_running = False
                    all_stopped = False

            if any_vm and lab_env.status not in ('provisioning', 'cleanup'):
                if all_running:
                    if lab_env.status != 'active' or lab_env.stopped_at is not None:
                        lab_env.status = 'active'
                        lab_env.stopped_at = None
                        lab_env.last_seen_at = timezone.now()
                        lab_env.save(update_fields=['status', 'stopped_at', 'last_seen_at'])
                    return

                # Stop all VMs if in a degraded state
                if not all_stopped and lab_env.status != 'stopping':
                    self.stop_environment(lab_env)
                    return

                update_fields = []
                if lab_env.status != 'stopped':
                    lab_env.status = 'stopped'
                    update_fields.append('status')
                if lab_env.stopped_at is None:
                    lab_env.stopped_at = timezone.now()
                    update_fields.append('stopped_at')
                if update_fields:
                    lab_env.save(update_fields=update_fields)

        except Exception:
            logger.exception("Error syncing VM status env_id=%s", lab_env.id)
            raise

    def get_vm_console_ticket(self, node, vmid):
        """
        Get console access ticket for a VM (for binary VNC).
        """
        try:
            self._authenticate()
            
            ticket_data = self.proxmox.nodes(node).qemu(vmid).vncproxy.post(
                websocket=1
            )
            
            return {
                'ticket': ticket_data['ticket'],
                'port': ticket_data['port'],
                'cert': ticket_data.get('cert', ''),
                'user': ticket_data.get('user', os.environ.get('PROXMOX_USER'))
            }
        except Exception:
            logger.exception("Error getting console ticket node=%s vmid=%s", node, vmid)
            raise

    def get_vm_node(self, vmid: int) -> str:
        """
        Returns the node name on which the given VMID currently resides.
        """
        try:
            resources = self.proxmox.cluster.resources.get(type='vm')
            for r in resources:
                try:
                    if int(r.get('vmid')) == int(vmid):
                        node = r.get('node')
                        if node:
                            return node
                except (TypeError, ValueError):
                    continue
            return self.get_node()
        except Exception:
            logger.exception("Error resolving node for VM vmid=%s", vmid)
            raise

    async def a_get_auth_cookie(self):
        return await asyncio.to_thread(self.get_auth_cookie)
    
    async def a_get_vm_node(self, vmid: int) -> str:
        return await asyncio.to_thread(self.get_vm_node, vmid)
    
    async def a_get_vm_console_ticket(self, node: str, vmid: int) -> dict:
        return await asyncio.to_thread(self.get_vm_console_ticket, node, vmid)
    
