import os
from proxmoxer import ProxmoxAPI
from django.db import transaction, IntegrityError
from dotenv import load_dotenv
from .utils import AdvisoryLock, slugify
from .models import LabEnvironment, TaskVMConfiguration, Network

# take environment variables
load_dotenv()


class ProxmoxManager:
    # Constants
    LOCK_TIMEOUT = 120
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
                    # TODO Create network here

                    # 2. Create the lab environment record
                    lab_env = LabEnvironment.objects.create(
                        user=user,
                        task=task,
                        network=network
                    )
                    
                    # 3. Create all VMs for env

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
                    #TODO check if cleanup is needed here
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