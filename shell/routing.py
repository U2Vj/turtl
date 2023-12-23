from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('shell', consumers.ShellConsumer.as_asgi()),
]
