from apps.core.services.status import *
from apps.core.services.generators import invoice_id_generator, receipt_no_generator
from .models import Invoice, InvoiceProduct, InvoiceReceipt


def m2m_changed_income_product(sender, instance: Invoice, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        products = instance.products.all()
        total = 0
        for x in products:
            total += x.selling_price
        if instance.subtotal != total:
            instance.subtotal = total
            instance.save()
m2m_changed.connect(m2m_changed_income_product, sender=Invoice.products.through)


@receiver(post_save, sender=Invoice)
def post_save_outlet_member(sender, instance: Invoice, created, **kwargs):
    if created:
        instance.expire_in = timezone.now() + timedelta(days=settings.INVOICE_EXPIRE_DAY)
        if instance.invoice_id is None or instance.invoice_id == "":
            instance.invoice_id = invoice_id_generator(instance=instance)
        instance.save()


@receiver(post_save, sender=InvoiceProduct)
def post_save_invoice_product(sender, instance: InvoiceProduct, created, **kwargs):
    if created:
        instance.total = instance.count * instance.product.selling_price
        instance.save()


@receiver(post_save, sender=InvoiceReceipt)
def post_save_invoice_product(sender, instance: InvoiceReceipt, created, **kwargs):
    if created:
        instance.receipt_no = receipt_no_generator(instance=instance)
        if instance.pay_type == InvoiceReceiptType.CASH_CARD:
            instance.total = instance.amount_cash + instance.amount_card
        instance.save()

