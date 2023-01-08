from apps.core.models import TimestampedModel
from apps.accounts.models import User
from apps.billings.models import BillingAccount
from apps.outlets.models import Currency, Outlet
from apps.products.models import OutletProduct
from apps.core.services.status import *


class Invoice(TimestampedModel):
    """
     ИНВОЙС ПРОДАЖИ
     счет фактура, накладная, квитанция
    """
    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE)
    invoice_id = models.CharField(max_length=120, unique=True)
    seller = models.ForeignKey(BillingAccount, on_delete=models.PROTECT, related_name="seller_bln")  # кассир
    buyer = models.ForeignKey(BillingAccount, on_delete=models.PROTECT, related_name="buyer_bln")  # покупатель
    products = models.ManyToManyField(
        OutletProduct, blank=True, through='InvoiceProduct', related_name='invoice_products'
    )
    subtotal = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    total = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    comment = models.TextField(blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    expire_in = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(choices=InvoiceStatus.choices, default=InvoiceStatus.DRAFT)

    class Meta:
        verbose_name_plural = "    Invoices"
        ordering = ['id']

    def __str__(self):
        return f"ID: {self.id} / {self.invoice_id}"

    def confirm_receipt(self, hook, msg):
        qs = self.invoice_receipt.filter(invoice_id=self.id)
        if qs.exists():
            qs.update(status=InvoiceCheckStatus.COMPLETED)
            hook(message=msg)

    def get_invoice_receipt(self):
        """ квитанция """
        return self.invoice_receipt.get(invoice_id=self.id)


class InvoiceProduct(TimestampedModel):
    count = models.PositiveSmallIntegerField(default=1)
    product = models.ForeignKey(OutletProduct, on_delete=models.CASCADE, related_name="through_invoice_product")
    total = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)  # quantity * product.selling_price
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "   InvoiceProducts"
        ordering = ['id']

    def __str__(self):
        return f"{self.id} / {self.invoice.invoice_id} / {self.count}"


class InvoiceReceipt(TimestampedModel):
    """ квитанция: для каждого типа оплаты [CASH, CARD, CASH_CARD, CREDIT]"""
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="invoice_receipt")  # квитанция
    receipt_no = models.CharField(max_length=120, unique=True)
    pay_type = models.IntegerField(choices=InvoiceReceiptType.choices, default=InvoiceReceiptType.CASH)
    amount_cash = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    amount_card = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    total = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    status = models.IntegerField(choices=InvoiceCheckStatus.choices, default=InvoiceCheckStatus.DRAFT)

    class Meta:
        verbose_name_plural = "  InvoiceReceipts"
        ordering = ['id']

    def __str__(self):
        return f"{self.id} / {self.invoice.invoice_id}"


class OutletExpense(TimestampedModel):
    """ расход магазина """
    outlet = models.ForeignKey(Outlet, on_delete=models.PROTECT, related_name="shop_expense")
    amount = models.DecimalField(default=0.0, max_digits=15, decimal_places=2)
    currency = models.IntegerField(choices=CurrencyType.choices, default=CurrencyType.UZS)

    def __str__(self):
        return str(self.amount)
