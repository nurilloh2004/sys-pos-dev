from django.apps import AppConfig


class OutletsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.outlets'

    def ready(self):
        # signals are imported, so that they are defined and can be used
        import apps.outlets.signal
