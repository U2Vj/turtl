from proxmoxer import ProxmoxAPI
import os

class ProxmoxManager:
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
        
    