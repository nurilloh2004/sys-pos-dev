from django.apps import AppConfig


class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.dashboard'

    def ready(self):
        # signals are imported, so that they are defined and can be used
        import apps.dashboard.signal
