from django.apps import AppConfig


class BillingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.billings'

    def ready(self):
        # signals are imported, so that they are defined and can be used
        import apps.billings.signal
