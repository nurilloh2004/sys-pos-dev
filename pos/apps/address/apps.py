from django.apps import AppConfig


class AddressConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.address'

    def ready(self):
        # signals are imported, so that they are defined and can be used
        import apps.address.signal
