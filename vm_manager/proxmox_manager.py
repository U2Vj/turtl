import os
import time
import threading
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
            # Initialize Proxmox API connection
            self.proxmox = ProxmoxAPI(
                host=os.environ.get('PROXMOX_HOST'),
                user=os.environ.get('PROXMOX_USER'),
                password=os.environ.get('PROXMOX_PASSWORD'),
                verify_ssl=False
            )
        except Exception as e:
            print(f"Failed to connect to Proxmox: {e}")
            raise e
        
    # Helper functions
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

                    return lab_env

            except Exception as e:
                print(f"Error creating lab environment for task : {task.title}")
                #TODO Cleanup here
    
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
                ci_user = 'root'
                ci_password = 'changeme'

                self.configure_vm(
                    node=node,
                    vm_id=vmid,
                    storage=storage,
                    ci_user=ci_user,
                    ci_password=ci_password,
                    bridge=bridge_name,
                    ip_address=ip_address
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

    def configure_vm(self, node, vm_id, storage, ci_user, ci_password, bridge, ip_address):
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
                'serial0': 'socket',
                'vga': 'serial0',
                'cicustom': 'user=local:snippets/user-data.yaml'
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
