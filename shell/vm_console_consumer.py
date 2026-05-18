import asyncio
import base64
import logging
import os
import ssl
import urllib.parse

import websockets
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache
from catalog.models import Task
from vm_manager.proxmox import ProxmoxManager
from vm_manager.access import user_can_access_task_vm
from vm_manager.models import VirtualMachine

logger = logging.getLogger("vm_manager.console")

class VMConsoleConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.proxmox_ws = None
        self.forward_task = None
    
    async def connect(self):
        self.task_id = self.scope['url_route']['kwargs']['task_id']
        self.user = self.scope['user']
        self.user_group = None

        if not self.user.is_authenticated:
            logger.warning("Unauthenticated user attempted VM console connection")
            await self.close()
            return

        if not await self.can_access_task_vm():
            logger.warning(
                "Forbidden VM console access user_id=%s task_id=%s",
                getattr(self.user, "id", None),
                self.task_id,
            )
            await self.close()
            return

        user_vm = await self.get_user_vm()
        if not user_vm:
            logger.warning(
                "No VM found for console connection user_id=%s task_id=%s",
                getattr(self.user, "id", None),
                self.task_id,
            )
            await self.close()
            return

        logger.info(
            "Found VM for console connection user_id=%s task_id=%s vmid=%s",
            getattr(self.user, "id", None),
            self.task_id,
            user_vm.vmid,
        )

        requested = self.scope.get('subprotocols', []) or []
        if 'binary' in requested:
            selected = 'binary'
        elif 'base64' in requested:
            selected = 'base64'
        else:
            selected = None

        max_connections = int(os.environ.get('WS_MAX_PARALLEL_PER_USER', '3'))
        count = await self._incr_user_ws_count(self.user.id)
        if count > max_connections:
            logger.warning(
                "WS connection limit exceeded user_id=%s count=%s max=%s",
                self.user.id, count, max_connections,
            )
            await self._decr_user_ws_count(self.user.id)
            await self.accept(subprotocol=selected)
            await self.close(code=4429)
            return

        try:
            self.user_group = f"user_{self.user.id}"
            await self.channel_layer.group_add(self.user_group, self.channel_name)
            await self.accept(subprotocol=selected)
        except BaseException:
            await self._decr_user_ws_count(self.user.id)
            raise
        
        self._ws_count_incremented = True
        logger.debug(
            "Client WebSocket accepted user_id=%s task_id=%s subprotocol=%s",
            getattr(self.user, "id", None),
            self.task_id,
            selected,
        )
        
        try:
            await self.connect_to_proxmox(user_vm)
        except Exception:
            logger.exception(
                "Failed to set up Proxmox console connection user_id=%s task_id=%s vmid=%s",
                getattr(self.user, "id", None),
                self.task_id,
                user_vm.vmid,
            )
            await self.close()
    
    async def connect_to_proxmox(self, user_vm):
        pm = ProxmoxManager()
        
        ticket = None
        vnc_port = None
        for proto in (self.scope.get('subprotocols', []) or []):
            if isinstance(proto, str) and proto.startswith('vnc.'):
                encoded = proto[4:]
                try:
                    padding = '=' * (-len(encoded) % 4)
                    ticket = base64.urlsafe_b64decode((encoded + padding).encode('ascii')).decode('utf-8')
                except Exception:
                    logger.warning("Invalid VNC ticket subprotocol payload")
            elif isinstance(proto, str) and proto.startswith('vncport.'):
                vnc_port = proto[8:]

        if not ticket or not vnc_port:
            logger.warning("Missing VNC ticket/port in websocket subprotocols")
            await self.close()
            return

        # Determine the correct node for this VM
        try:
            node = await pm.a_get_vm_node(user_vm.vmid)
        except Exception:
            logger.exception("Failed to determine VM node vmid=%s", user_vm.vmid)
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

        logger.debug("Connecting to Proxmox WebSocket vmid=%s node=%s", user_vm.vmid, node)
        
        # Setup SSL context 
        ca_path = os.environ.get('PROXMOX_CA_PATH')
        verify_env = os.environ.get('PROXMOX_VERIFY_SSL', 'true').strip().lower()
        ssl_context = ssl.create_default_context()
        ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2
        
        if verify_env in ('false', '0'):
            logger.warning(
                "SSL certificate verification is DISABLED for Proxmox WebSocket connections "
                "because PROXMOX_VERIFY_SSL is set to '%s'. This configuration is insecure and "
                "should only be used for development or testing environments. host=%s",
                verify_env,
                proxmox_host,
            )
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
        elif ca_path:
            ssl_context.load_verify_locations(cafile=ca_path)

        if self._is_ip(proxmox_host):
            ssl_context.check_hostname = False
        
        # Prepare API token authentication for WebSocket
        api_token = pm.get_api_token()

        headers = {
            "Authorization": f"PVEAPIToken={api_token}",
            "Origin": f"https://{proxmox_host}:8006",
            "Host": f"{proxmox_host}:8006",
        }
        
        try:

            verify_off = verify_env in ('false', '0')
            self.proxmox_ws = await websockets.connect(
                proxmox_url, 
                ssl=ssl_context,
                additional_headers=headers,
                subprotocols=['binary'],
                server_hostname=None if verify_off or self._is_ip(proxmox_host) else proxmox_host,
            )
            logger.info("Successfully connected to Proxmox WebSocket vmid=%s node=%s", user_vm.vmid, node)
        except Exception:
            logger.exception("Failed to connect to Proxmox WebSocket vmid=%s node=%s", user_vm.vmid, node)
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

    @staticmethod
    @sync_to_async
    def _incr_user_ws_count(user_id):
        key = f"ws_console_count_{user_id}"
        try:
            return cache.incr(key)
        except ValueError:
            cache.set(key, 1, timeout=5000)
            return 1

    @staticmethod
    @sync_to_async
    def _decr_user_ws_count(user_id):
        key = f"ws_console_count_{user_id}"
        try:
            cache.decr(key)
        except ValueError:
            pass
    
    async def disconnect(self, close_code):
        if getattr(self, '_ws_count_incremented', False):
            await self._decr_user_ws_count(self.user.id)
        if self.forward_task:
            self.forward_task.cancel()
        if self.proxmox_ws:
            await self.proxmox_ws.close()
        if self.user_group:
            await self.channel_layer.group_discard(self.user_group, self.channel_name)
        logger.debug(
            "VM console disconnected user_id=%s task_id=%s close_code=%s",
            getattr(self.user, "id", None),
            getattr(self, "task_id", None),
            close_code,
        )

    async def force_disconnect(self, event):
        logger.info(
            "Force-disconnecting VM console user_id=%s task_id=%s",
            getattr(self.user, "id", None),
            getattr(self, "task_id", None),
        )
        await self.close(code=4401)
    
    async def receive(self, text_data=None, bytes_data=None):
        # Forward to Proxmox
        if self.proxmox_ws:
            try:
                if bytes_data:
                    await self.proxmox_ws.send(bytes_data)
                elif text_data:
                    await self.proxmox_ws.send(text_data)
            except Exception:
                logger.exception(
                    "Error forwarding message to Proxmox user_id=%s task_id=%s",
                    getattr(self.user, "id", None),
                    getattr(self, "task_id", None),
                )
    
    async def forward_messages(self):
        """Forward messages from Proxmox to client"""
        try:
            async for message in self.proxmox_ws:
                if isinstance(message, bytes):
                    await self.send(bytes_data=message)
                else:
                    await self.send(text_data=message)
        except asyncio.CancelledError:
            logger.debug(
                "Forwarding task cancelled user_id=%s task_id=%s",
                getattr(self.user, "id", None),
                getattr(self, "task_id", None),
            )
            raise
        except websockets.exceptions.ConnectionClosed:
            logger.info(
                "Proxmox WebSocket connection closed user_id=%s task_id=%s",
                getattr(self.user, "id", None),
                getattr(self, "task_id", None),
            )
            await self.close()
        except Exception:
            logger.exception(
                "Error in VM console forward_messages user_id=%s task_id=%s",
                getattr(self.user, "id", None),
                getattr(self, "task_id", None),
            )
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
                logger.debug("Found USER_SHELL VM vm_name=%s vmid=%s", vm.name, vm.vmid)
            return vm
        
        return await get_vm()

    async def can_access_task_vm(self):
        from asgiref.sync import sync_to_async

        @sync_to_async
        def can_access():
            task = Task.objects.select_related('project__classroom').filter(id=self.task_id).first()
            if not task:
                return False
            return user_can_access_task_vm(self.user, task)

        return await can_access()
