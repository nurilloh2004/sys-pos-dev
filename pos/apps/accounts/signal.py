from django.conf import settings
from .models import User, ActivationSMSCode
from apps.billings.models import BillingAccount, UserBalance
from apps.core.services.generators import random_activation_sms_code
from apps.core.services.status import *


def post_save_user_create_receiver(sender, instance: User, created, *args, **kwargs):
    if created:
        BillingAccount.objects.create(user_id=instance.id)
        UserBalance.objects.create(user_id=instance.id)
post_save.connect(post_save_user_create_receiver, sender=User)


def post_save_activation_code(sender, instance: ActivationSMSCode, created, *args, **kwargs):
    if created:
        instance.code = random_activation_sms_code()
        instance.expires_in += timedelta(minutes=settings.SMS_TIMEOUT_MIN)
        instance.save()
        # instance.send_sms()
post_save.connect(post_save_activation_code, sender=ActivationSMSCode)