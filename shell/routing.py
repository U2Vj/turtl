from django.urls import re_path
from . import vm_console_consumer, consumers

websocket_urlpatterns = [
    re_path(r'^shell/ws/vm-console/(?P<task_id>\d+)/$', vm_console_consumer.VMConsoleConsumer.as_asgi()),
    re_path(r'^shell/ws/$', consumers.ShellConsumer.as_asgi()),
]