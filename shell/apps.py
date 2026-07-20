from django.apps import AppConfig


class ShellConfig(AppConfig):
    name = 'shell'

    def ready(self):
        from . import signals
