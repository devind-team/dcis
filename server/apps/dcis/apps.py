from django.apps import AppConfig


class DcisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.dcis'

    def ready(self):
        import apps.dcis.signals
