# mysite/asgi.py
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "turtl.settings")

from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application()

from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter
import shell.routing
from shell.auth import jwt_auth_middleware_stack


application = ProtocolTypeRouter({
  "http": django_asgi_app,
  "websocket": AllowedHostsOriginValidator(
        jwt_auth_middleware_stack(
            URLRouter(
                shell.routing.websocket_urlpatterns
            )
        )
    ),
})