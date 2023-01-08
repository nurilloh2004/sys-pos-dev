from django.apps import AppConfig


class UploadConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.upload'

    def ready(self):
        # signals are imported, so that they are defined and can be used
        import apps.upload.signal
