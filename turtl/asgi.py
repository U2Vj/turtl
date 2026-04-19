# mysite/asgi.py
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "turtl.settings")

from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application()

from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter
import shell.routing
from shell.auth import JwtAuthMiddlewareStack


application = ProtocolTypeRouter({
  "http": django_asgi_app,
  "websocket": AllowedHostsOriginValidator(
        JwtAuthMiddlewareStack(
            URLRouter(
                shell.routing.websocket_urlpatterns
            )
        )
    ),
})