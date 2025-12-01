import asyncio
import websockets
import ssl
import urllib.parse
from channels.generic.websocket import AsyncWebsocketConsumer
from vm_manager.proxmox_manager import ProxmoxManager
from vm_manager.models import VirtualMachine
import os

class VMConsoleConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.proxmox_ws = None
        self.forward_task = None
    
    async def connect(self):
        self.task_id = self.scope['url_route']['kwargs']['task_id']
        self.user = self.scope['user']
        
        if not self.user.is_authenticated:
            print(f"Unauthenticated user attempted connection")
            await self.close()
            return
        
        
        # Get user vm
        user_vm = await self.get_user_vm()
        if not user_vm:
            print(f"No VM found for user {self.user}")
            await self.close()
            return
        
        print(f"Found VM {user_vm.vmid} for user {self.user}")

        requested = self.scope.get('subprotocols', []) or []
        selected = 'binary' if 'binary' in requested else ( 'base64' if 'base64' in requested else None )
        await self.accept(subprotocol=selected)
        print("Client WebSocket accepted")
        
        try:
            await self.connect_to_proxmox(user_vm)
        except Exception as e:
            print(f"Failed to setup Proxmox connection: {e}")
            await self.close()
    
    async def connect_to_proxmox(self, user_vm):
        pm = ProxmoxManager()
        
        # Parse query params from client WS (ticket+port expected)
        try:
            raw_qs = (self.scope.get('query_string') or b'').decode('utf-8')
            qs = urllib.parse.parse_qs(raw_qs)
        except Exception:
            qs = {}

        ticket = (qs.get('ticket') or [None])[0]
        vnc_port = (qs.get('port') or [None])[0]

        # Determine the correct node for this VM
        try:
            node = await pm.a_get_vm_node(user_vm.vmid)
        except Exception as e:
            print(f"Failed to determine VM node: {e}")
            await self.close()
            return

        # If ticket/port were not provided by client, obtain them once here
        if not ticket or not vnc_port:
            try:
                ticket_data = await pm.a_get_vm_console_ticket(node, user_vm.vmid)
                ticket = ticket_data['ticket']
                vnc_port = ticket_data['port']
            except Exception as e:
                print(f"Failed to obtain VNC ticket/port: {e}")
                await self.close()
                return

        # Parse PROXMOX_HOST to extract hostname without port
        proxmox_host = os.environ.get('PROXMOX_HOST')
        if proxmox_host and ':' in proxmox_host:
            proxmox_host = proxmox_host.split(':')[0]
        
        # URL encode the ticket
        encoded_ticket = urllib.parse.quote(ticket)
        
        # Build WebSocket URL to Proxmox
        proxmox_url = f"wss://{proxmox_host}:8006/api2/json/nodes/{node}/qemu/{user_vm.vmid}/vncwebsocket"
        proxmox_url += f"?port={vnc_port}&vncticket={encoded_ticket}"

        # Avoid logging sensitive details like tickets/URLs
        print("Connecting to Proxmox WebSocket")
        
        # Setup SSL context 
        ca_path = os.environ.get('PROXMOX_CA_PATH')
        verify_env = os.environ.get('PROXMOX_VERIFY_SSL', 'true').strip().lower()
        ssl_context = ssl.create_default_context()
        
        if verify_env in ('false', '0'):
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
        elif ca_path:
            ssl_context.load_verify_locations(cafile=ca_path)

        if self._is_ip(proxmox_host):
            ssl_context.check_hostname = False
        
        # Prepare Proxmox authentication cookie
        try:
            pve_cookie = await pm.a_get_auth_cookie()
        except Exception as e:
            print(f"Failed to authenticate with Proxmox: {e}")
            await self.close()
            return

        headers = {
            "Cookie": f"PVEAuthCookie={pve_cookie}",
            "Origin": f"https://{proxmox_host}:8006",
            "Host": f"{proxmox_host}:8006",
        }
        
        try:

            verify_off = verify_env in ('false', '0')
            self.proxmox_ws = await websockets.connect(
                proxmox_url, 
                ssl=ssl_context,
                extra_headers=headers,
                subprotocols=['binary'],
                server_hostname=None if verify_off or self._is_ip(proxmox_host) else proxmox_host,
            )
            print("Successfully connected to Proxmox WebSocket")
        except Exception as e:
            print(f"Failed to connect to Proxmox WebSocket: {e}")
            await self.close()
            return
        
        # Start forwarding
        self.forward_task = asyncio.create_task(self.forward_messages())

    def _is_ip(self, host: str) -> bool:
        parts = host.split(".")
        if len(parts) != 4:
            return False
        try:
            return all(0 <= int(p) <= 255 for p in parts)
        except ValueError:
            return False
    
    async def disconnect(self, close_code):
        if self.forward_task:
            self.forward_task.cancel()
        if self.proxmox_ws:
            await self.proxmox_ws.close()
    
    async def receive(self, text_data=None, bytes_data=None):
        # Forward to Proxmox
        if self.proxmox_ws:
            try:
                if bytes_data:
                    await self.proxmox_ws.send(bytes_data)
                elif text_data:
                    await self.proxmox_ws.send(text_data)
            except Exception as e:
                print(f"Error forwarding to Proxmox: {e}")
    
    async def forward_messages(self):
        """Forward messages from Proxmox to client"""
        try:
            async for message in self.proxmox_ws:
                if isinstance(message, bytes):
                    await self.send(bytes_data=message)
                else:
                    await self.send(text_data=message)
        except asyncio.CancelledError:
            pass
        except websockets.exceptions.ConnectionClosed:
            print("Proxmox WebSocket connection closed")
            await self.close()
        except Exception as e:
            print(f"Error in forward_messages: {e}")
            await self.close()

    async def get_user_vm(self):
        from asgiref.sync import sync_to_async
        
        @sync_to_async
        def get_vm():
            vm = VirtualMachine.objects.filter(
                lab_environment__user=self.user,
                lab_environment__task_id=self.task_id,
                template__purpose='USER_SHELL'
            ).select_related('lab_environment').first()
            
            if vm:
                print(f"Found VM: {vm.name} (ID: {vm.vmid})")
            return vm
        
        return await get_vm()
