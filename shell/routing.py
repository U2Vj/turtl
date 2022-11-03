from django.urls import path, re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/shell/(?P<room_name>\w+)/$', consumers.ShellConsumer.as_asgi()),
    path('shell', consumers.ShellConsumer.as_asgi()),
]
