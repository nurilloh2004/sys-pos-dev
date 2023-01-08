from apps.core.services.status import *
from .models import Outlet, OutletCashBox, Currency, OutletMember, OutletCustomer


@receiver(post_save, sender=Outlet)
def post_save_obj(sender, instance: Outlet, created, **kwargs):
    if created:
        OutletCashBox.objects.create(outlet_id=instance.id, name=instance.name)
        instance.create_outlet_member()
        if instance.currency is None:
            instance.currency_id = Currency.get_currency_uzs().id

        if Outlet.objects.filter(user=instance.user, type=OutletType.MAIN).count() < 1:
            instance.type = OutletType.MAIN
        instance.save()


@receiver(post_save, sender=OutletMember)
def post_save_obj(sender, instance: OutletMember, created, **kwargs):
    if created:

        if instance.user.id == instance.outlet.owner.id:
            instance.type = OutletMemberType.OWNER
            instance.save()


@receiver(post_save, sender=OutletCustomer)
def post_save_obj(sender, instance: OutletCustomer, created, **kwargs):
    if created:
        instance.balance_id = instance.user.user_balance.id
        instance.save()

