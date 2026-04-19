# mysite/asgi.py
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "turtl.settings")

from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import shell.routing
from shell.auth import JwtAuthMiddlewareStack



application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AllowedHostsOriginValidator(
        JwtAuthMiddlewareStack(
            URLRouter(
                shell.routing.websocket_urlpatterns
            )
        )
    ),
})