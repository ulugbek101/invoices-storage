from django.apps import AppConfig


class AppMainConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app_main"
    verbose_name = "Товары и Поставки"

    def ready(self):
        from . import signals
