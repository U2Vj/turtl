# mysite/asgi.py
import os

from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import shell.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "turtl.settings")



application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                shell.routing.websocket_urlpatterns
            )
        )
    ),
})