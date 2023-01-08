from apps.core.services.status import *
from apps.core.services.generators import invoice_id_generator
from .models import Transaction


@receiver(post_save, sender=Transaction)
def post_save_transaction(sender, instance: Transaction, created, **kwargs):
    if created:
        if not instance.transaction_id:
            instance.transaction_id = uuid.uuid4()
            instance.save()


