from django.apps import AppConfig

class LegaciesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "legacies"

    # def ready(self):
    #     import legacies.signals  # noqa

