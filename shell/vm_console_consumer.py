# vm_console_consumer.py
import asyncio
import websockets
import ssl
import urllib.parse
from channels.generic.websocket import AsyncWebsocketConsumer
from vm_manager.proxmox_manager import ProxmoxManager # Sie müssen diese Klasse anpassen
from vm_manager.models import LabEnvironment, VirtualMachine
import os

class VMConsoleConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.proxmox_ws = None
        self.forward_task = None
        self.receive_task = None
        self.should_close = False
    
    async def connect(self):
        self.task_id = self.scope['url_route']['kwargs']['task_id']
        self.user = self.scope['user']
        
        # Benutzer-VM holen
        user_vm = await self.get_user_vm()
        if not user_vm:
            await self.close()
            return
        
        # Zuerst die Client-Verbindung akzeptieren
        await self.accept() 
        print("Client WebSocket accepted")
        
        # Dann die Verbindung zu Proxmox herstellen
        try:
            await self.connect_to_proxmox(user_vm)
        except Exception as e:
            print(f"Failed to setup Proxmox connection: {e}")
            await self.close()
    
    async def connect_to_proxmox(self, user_vm):
        # Annahme: ProxmoxManager hat eine Methode, die den Referer-Header unterstützt
        pm = ProxmoxManager()
        
        # Get console ticket from Proxmox
        pm = ProxmoxManager()
        ticket_data = pm.get_vm_console_ticket('turtlmaster', user_vm.vmid)
        
        # Parse PROXMOX_HOST to extract hostname without port
        proxmox_host = os.environ.get('PROXMOX_HOST')
        if ':' in proxmox_host:
            proxmox_host = proxmox_host.split(':')[0]
        
        # Extract port number from ticket
        vnc_port = ticket_data['port']
        
        # URL encode the ticket
        encoded_ticket = urllib.parse.quote(ticket_data['ticket'])
        
        # Build WebSocket URL with properly encoded parameters
        proxmox_url = f"wss://{proxmox_host}:8006/api2/json/nodes/turtlmaster/qemu/{user_vm.vmid}/vncwebsocket"
        proxmox_url += f"?port={vnc_port}&vncticket={encoded_ticket}"
        
        print(f"Connecting to Proxmox WebSocket: {proxmox_url}")
        
        # Setup SSL context
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        # Prepare headers with proper authentication
        headers = {
            "Cookie": f"PVEAuthCookie={ticket_data['pve_auth_cookie']}",
            "Origin": f"https://{proxmox_host}:8006",
            "Host": f"{proxmox_host}:8006",
        }
        
        try:
            self.proxmox_ws = await websockets.connect(
                proxmox_url, 
                ssl=ssl_context,
                extra_headers=headers,
                subprotocols=['binary']
            )
            print("Successfully connected to Proxmox WebSocket")
            
            # Send VNC auth info to the client as proper JSON
            import json
            auth_info = {
                'type': 'vnc_auth',
                'ticket': ticket_data['ticket'],
                'pve_auth_cookie': ticket_data['pve_auth_cookie']
            }
            await self.send(text_data=json.dumps(auth_info))
        except Exception as e:
            print(f"Failed to connect to Proxmox WebSocket: {e}")
            await self.close()
            return
        
        # Start forwarding
        self.forward_task = asyncio.create_task(self.forward_messages())
    
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
        """Get USER_SHELL VM for this task/user"""
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

