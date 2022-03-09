"""Settings for core application."""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Core settings."""

    name = 'apps.core'

    def ready(self):
        """Start function when core app started."""
        import apps.core.signals # noqa
