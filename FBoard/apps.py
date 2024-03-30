from django.apps import AppConfig


class FboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'FBoard'

    def ready(self):
        from . import signals

