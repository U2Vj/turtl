from django.apps import AppConfig


class CatalogConfig(AppConfig):
    name = 'catalog'

    def ready(self):
        # noinspection PyUnresolvedReferences
        from . import signals
