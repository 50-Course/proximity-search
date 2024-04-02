from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "proximity_apps.core"

    def ready(self) -> None:
        from . import signals
