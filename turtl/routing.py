from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import shell.routing

# TODO: Add jwt authentication middleware to authenticate request to docker
# https://stackoverflow.com/questions/43392889/how-do-you-authenticate-a-websocket-with-token-authentication-on-django-channels

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            shell.routing.websocket_urlpatterns
        )
    ),
})
