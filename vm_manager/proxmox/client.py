import os
import asyncio
import logging
from proxmoxer import ProxmoxAPI
from dotenv import load_dotenv
from django.conf import settings

load_dotenv()
logger = logging.getLogger(__name__)


class ProxmoxClient:
    # Locking constants
    LOCK_TIMEOUT = 120
    POLL_INTERVAL = 2
    LOCK_ACQUIRE_TIMEOUT = 30

    def __init__(self):
        try:
            host = os.environ.get('PROXMOX_HOST')
            user = os.environ.get('PROXMOX_USER')
            token_name = os.environ.get('PROXMOX_TOKEN_NAME')
            token_value = os.environ.get('PROXMOX_TOKEN_VALUE')
            verify_param = self._get_verify_param()

            self.proxmox = ProxmoxAPI(
                host=host,
                user=user,
                token_name=token_name,
                token_value=token_value,
                verify_ssl=verify_param,
            )

            # Store token string for WebSocket authentication
            self._api_token = f"{user}!{token_name}={token_value}"
        except Exception:
            logger.exception("Failed to connect to Proxmox API")
            raise

    def _get_verify_param(self):

        verify_env = os.environ.get('PROXMOX_VERIFY_SSL')
        if verify_env == 'false':
            return False

        ca_path = os.environ.get('PROXMOX_CA_PATH') or os.path.join(settings.BASE_DIR, 'proxmox-ca.pem')
        return ca_path if os.path.isfile(ca_path) else True
    
    def get_api_token(self):
        """
        Returns the PVEAPIToken string for WebSocket authentication.
        """
        return self._api_token

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

    def get_vm_console_ticket(self, node, vmid):
        """
        Get console access ticket for a VM (for binary VNC).
        """
        try:
            ticket_data = self.proxmox.nodes(node).qemu(vmid).vncproxy.post(
                websocket=1
            )

            return {
                'ticket': ticket_data['ticket'],
                'port': ticket_data['port'],
                'cert': ticket_data.get('cert', ''),
                'user': ticket_data.get('user')
            }
        except Exception:
            logger.exception("Error getting console ticket node=%s vmid=%s", node, vmid)
            raise

    async def a_get_vm_node(self, vmid: int) -> str:
        return await asyncio.to_thread(self.get_vm_node, vmid)

    async def a_get_vm_console_ticket(self, node: str, vmid: int) -> dict:
        return await asyncio.to_thread(self.get_vm_console_ticket, node, vmid)
