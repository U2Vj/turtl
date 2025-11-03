import os
import time
import asyncio
import requests
from concurrent.futures import ThreadPoolExecutor
from proxmoxer import ProxmoxAPI
from django.db import transaction, IntegrityError
from dotenv import load_dotenv
from .utils import AdvisoryLock, slugify, format_ip
from .models import LabEnvironment, TaskVMConfiguration, Network, VirtualMachine

# take environment variables
load_dotenv()

# Global ThreadPool
_thread_pool = ThreadPoolExecutor(max_workers=10, thread_name_prefix="proxmox_ops")

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
            # Add attributes to store auth credentials
            self.auth_cookie = None
            self.csrf_token = None
        except Exception as e:
            print(f"Failed to connect to Proxmox: {e}")
            raise e

    def _authenticate(self):
        """
        Ensures the manager is authenticated and has a valid cookie and CSRF token.
        If not authenticated, it will perform a login request and store the credentials.
        """
        if self.auth_cookie and self.csrf_token:
            return

        verify_param = self._get_verify_param()

        try:
            print("DEBUG: Authenticating with Proxmox...")
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
            self.csrf_token = login_data.get("CSRFPreventionToken", "")
            print("DEBUG: Successfully authenticated and stored credentials.")
        except requests.exceptions.RequestException as e:
            print(f"FATAL: Proxmox authentication failed: {e}")
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
            return True

    def get_node(self):
        """
        Get a available Proxmox node
        TODO: Add proper load balancing for multiple nodes
        """
        try:
            nodes = self.proxmox.nodes.get()
            for node in nodes:
                if node['status'] == 'online':
                    print(f"Found node: {node['node']}")
                    return node['node']
            raise Exception("No available nodes in cluster")
        except Exception as e:
            print(f"Error finding suitable node: {str(e)}")
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
                    print(f"Lab environment already exists for user {user.id} and task {task.id}")
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
                    lab_env.save()

                    return lab_env

            except Exception as e:
                print(f"Error creating lab environment for task : {task.title}")
                print(f"Exception: {str(e)}")
                #TODO Cleanup here
                raise e
    
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
                        except Exception as e:
                            print(f"Error creating bridge in Proxmox: {str(e)}")
                            raise

                        return network
                except IntegrityError as e:
                    if 'vlan_id' in str(e) and attempt < max_retries - 1:
                        print(f"VLAN ID {bridge_id} already exists, retrying... (attempt {attempt + 1}/{max_retries})")
                        # Short delay before retry to allow other transactions to complete
                        time.sleep(0.3)
                        continue
                    else:
                        print(f"Failed to allocate unique VLAN ID after {max_retries} attempts")
                        raise
    
    def create_bridge(self, node, bridge, cidr, gateway=None, autostart=True):
        """
        Creates a new Linux bridge in Proxmox and activates it directly.
        """
        try:
            existing = self.proxmox.nodes(node).network.get()
            if any(net.get('iface') == bridge for net in existing):
                print(f"Bridge '{bridge}' already exists. Skipping creation.")
                try:
                    self.proxmox.nodes(node).network(bridge).up.post()
                except Exception:
                    pass
                return
        except Exception as e:
            print(f"Error checking existing networks: {e}")
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
            print(f"Network '{bridge}' created: {result}")
            self.proxmox.nodes(node).network.put()
            print("Network configuration reloaded.")
        except Exception as e:
            print(f"Error creating network: {e}")

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
                vm_name = f"{slugify(lab_env.task.title)}-{slugify(lab_env.user.username)}-{slugify(template.name)}"
                ip_address = format_ip(vm_template_config.planned_ip_address, network)

                # Clone VM from template
                print(f"DEBUG: Cloning vom from template {template.template_id} to {vm_name} (ID: {vmid})")
                self.clone_vm(
                    node=node,
                    template_id=template.template_id,
                    new_id=vmid,
                    new_name=vm_name,
                    threaded_wait=False
                )

                bridge_name = f"vmbr{network.vlan_id}"

                print(f"DEBUG: Configuring VM {vmid} with networking")
                #TODO Set better and custom passwords for production use
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
                    print(f"DEBUG: Starting VM {vmid}")
                    self.proxmox.nodes(node).qemu(vmid).status.start.post()

                    # Update status
                    vm.status = 'running'
                    vm.save()
                
                return vm
            except Exception as e:
                print(f"Error provisioning VM: {e}")
                raise

    def clone_vm(self, node, template_id, new_id, new_name, linked_clone=True, threaded_wait=True):
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
            print(f"DEBUG: Clone command sent for VM {new_id}")
        except Exception as e:
            print(f"Debug: Error cloning template: {e}")
            raise

        print(f"DEBUG: Waiting for lock to be removed on VM {new_id}...")
        if threaded_wait:
            future = self.wait_for_unlock(node, new_id, threaded=True)
            return future
        else:
            self.wait_for_unlock(node, new_id)
            print(f"DEBUG: Lock removed from VM {new_id}")

    def wait_for_unlock(self, node, vm_id, timeout=None, interval=None, threaded=False):
        """
        Waits until the VM Lock is removed by Proxmox
        """
        if timeout is None:
            timeout = self.LOCK_TIMEOUT
        if interval is None:
            interval = self.POLL_INTERVAL

        def _wait():
            start = time.time()
            while True:
                locks = self.proxmox.nodes(node).qemu(vm_id).status.current.get().get('lock')
                if not locks:
                    return
                if time.time() - start > timeout:
                    raise TimeoutError(f"Timeout waiting for unlock of VM {vm_id}")
                time.sleep(interval)

        if threaded:
            future = _thread_pool.submit(_wait)
            return future
        else:
            _wait()

    def configure_vm(self, node, vm_id, storage, ci_user, ci_password, bridge, ip_address, cpu_cores, memory_mb):
        """
        Configures the Cloud-init, network and other VM options
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
            print(f"DEBUG: VM options set successfully for VM {vm_id}")
        except Exception as e:
            print(f"DEBUG: Error configuring VM {vm_id}: {str(e)}")
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
                node = self.get_node()

                with transaction.atomic():
                    for vm in lab_env.virtual_machines.select_for_update().all():
                        if vm.status != 'running':
                            # Start the VM
                            self.proxmox.nodes(node).qemu(vm.vmid).status.start.post()
                            # Update VM status
                            vm.status = 'running'
                            vm.save()
                return True
            except Exception as e:
                print(f"Error starting lab environment: {str(e)}")
                raise

    def stop_environment(self, lab_env):
        """
        Stops all VMs inside a lab environment
        """
        env_operation_lock = f"lab_env_operation_{lab_env.id}"

        with AdvisoryLock(env_operation_lock, timeout_seconds=self.LOCK_ACQUIRE_TIMEOUT) as acquired:
            if not acquired:
                raise TimeoutError(f"Could not acquire lock for starting environment {lab_env.id}")
            
            try:
                node = self.get_node()

                with transaction.atomic():
                    for vm in lab_env.virtual_machines.select_for_update().all():
                        if vm.status == 'running':
                            # Stop the VM
                            self.proxmox.nodes(node).qemu(vm.vmid).status.stop.post()
                            # Update VM status
                            vm.status = 'stopped'
                            vm.save()
                return True
            except Exception as e:
                print(f"Error starting lab environment: {str(e)}")
                raise

    def cleanup_environment(self, user, task, threaded=False):
        """
        Deletes all VMs and the network of a lab environment for a given user and task. Then deletes the lab environment.
        """

        def _cleanup():
            env_cleanup_lock = f"lab_env_cleanup_{user.id}_{task.id}"

            with AdvisoryLock(env_cleanup_lock, timeout_seconds=self.LOCK_ACQUIRE_TIMEOUT) as acquired:
                if not acquired:
                    print(f"Could not acquire lock for cleanup, skipping...")
                    return
                
                try:
                    # Get the lab environment
                    lab_env = LabEnvironment.objects.filter(user=user, task=task).first()
                    if not lab_env:
                        print(f"No lab environment found for user {user.id} and task {task.id}")
                        return
                    # Delete all VMs
                    for vm in lab_env.virtual_machines.all():
                        try:
                            node = self.get_node()
                            # Stop the VM
                            try:
                                self.proxmox.nodes(node).qemu(vm.vmid).status.stop.post()
                                # Wait for VM to stop
                                time.sleep(5)
                            except Exception as e:
                                print(f"Warning: Could not stop VM {vm.vmid}: {str(e)}")
                            self.proxmox.nodes(node).qemu(vm.vmid).delete()
                            # Delete VM from database
                            vm.delete()
                        except Exception as e:
                            print(f"Warning: Could not delete VM {vm.vmid}: {str(e)}")
                    
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
                                except Exception as e:
                                    print(f"Warning: Could not delete bridge {bridge_name}: {str(e)}")
    
                            # Delete network from database
                            lab_env.network.delete()
                        except Exception as e:
                            print(f"Warning: Error deleting network: {str(e)}")

                    # Delete lab environment
                    lab_env.delete()
                                
                except Exception as e:
                    print(f"Error during cleanup: {str(e)}")

        if threaded:
            future = _thread_pool.submit(_cleanup)
            return future
        else:
            _cleanup()

    def sync_vm_status(self, lab_env):
        """
        Synchronizes VM status with Proxmox for a lab environment
        """

        try:
            node = self.get_node()

            for vm in lab_env.virtual_machines.all():
                try:
                    # Get VM status from Proxmox
                    vm_status = self.proxmox.nodes(node).qemu(vm.vmid).status.current.get().get('status')

                    if vm.status != vm_status:
                        vm.status = vm_status
                        vm.save()
                except Exception as e:
                    print(f"Warning: Could not sync status for VM {vm.vmid}: {str(e)}")

        except Exception as e:
            print(f"Error  syncing VM status: {str(e)}")
            raise

    def get_vm_console_ticket(self, node, vmid):
        """
        Get console access ticket for a VM (for binary VNC).
        """
        try:
            self._authenticate() # Ensure we are logged in
            
            # Use the proxmoxer API which is already authenticated
            ticket_data = self.proxmox.nodes(node).qemu(vmid).vncproxy.post(
                websocket=1  # Enable websocket support
            )
            
            # Return all necessary authentication data
            return {
                'pve_auth_cookie': self.auth_cookie,
                'csrf_token': self.csrf_token,
                'ticket': ticket_data['ticket'],
                'port': ticket_data['port'],
                'cert': ticket_data.get('cert', ''),
                'user': ticket_data.get('user', os.environ.get('PROXMOX_USER'))
            }
        except Exception as e:
            print(f"Error getting console ticket: {e}")
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
            # Fallback: try first online node (may fail later if wrong)
            return self.get_node()
        except Exception as e:
            print(f"Error resolving node for VM {vmid}: {e}")
            # Bubble up so caller can decide
            raise

    async def a_authenticate(self):
        return await asyncio.to_thread(self._authenticate)
    
    async def a_get_auth_cookie(self):
        return await asyncio.to_thread(self.get_auth_cookie)
    
    async def a_get_vm_node(self, vmid: int) -> str:
        return await asyncio.to_thread(self.get_vm_node, vmid)
    
    async def a_get_vm_console_ticket(self, node: str, vmid: int) -> dict:
        return await asyncio.to_thread(self.get_vm_console_ticket, node, vmid)
    
