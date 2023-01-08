from apps.core.models import TimestampedModel
from apps.accounts.models import User
# from apps.outlets.models import Outlet, OutletCashBox
from apps.core.services.status import *


class BillingAccount(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="billing_account")
    name = models.CharField(max_length=50, blank=True)
    card_number = models.CharField(max_length=50, blank=True)
    expire_date = models.CharField(max_length=50, blank=True)
    token = models.CharField(max_length=50, blank=True)
    type = models.IntegerField(choices=BillingAccountType.choices, default=BillingAccountType.CUSTOMER)

    def __str__(self):
        return f"{self.user.phone}"

    class Meta:
        verbose_name_plural = "   BillingProfiles"
        ordering = ['-id']


class UserBalance(TimestampedModel):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name="user_balance")
    amount = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    is_blocked = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "  UserBalances"
        ordering = ['-id']

    def __str__(self):
        return f"ID: {self.id} / {self.amount}"

    def update_user_balance(self, plus=None, minus=None):
        if plus and minus is None:
            self.amount += plus
        if minus and plus is None:
            self.amount -= minus

        self.save(update_fields=('amount', 'updated_at'))


class Transfer(TimestampedModel):
    total = models.CharField(max_length=255)
    currency = models.IntegerField(choices=CurrencyType.choices, default=CurrencyType.UZS)
    # outlet = models.IntegerField(choices=OutletStatus.choices, default=OutletStatus.MAIN)

    class Meta:
        verbose_name_plural = "Transfers"
        ordering = ['id']

    def __str__(self):
        return f"ID: {self.id} / {self.total}"


class Transaction(TimestampedModel):
    transaction_id = models.CharField(max_length=255, blank=True, null=True)  # +
    invoice = models.ForeignKey("reports.Invoice", blank=True, null=True, on_delete=models.SET_NULL, related_name='transaction')

    origin = models.ForeignKey(BillingAccount, on_delete=models.PROTECT, related_name='origin_bln')
    destination = models.ForeignKey(BillingAccount, on_delete=models.PROTECT, related_name='destination_bln')

    pay_method = models.IntegerField(choices=PaymentMethod.choices, default=PaymentMethod.CASH)
    reason = models.IntegerField(choices=TransactionReason.choices, default=TransactionReason.BUYING)
    amount = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    status = models.IntegerField(choices=TransactionState.choices, default=TransactionState.CREATED)
    comment = models.TextField(blank=True)
    currency = models.IntegerField(choices=CurrencyType.choices, default=CurrencyType.UZS)
    balance_updated = models.BooleanField(default=False)
    created_time = models.CharField(max_length=255, blank=True)
    perform_time = models.DateTimeField(null=True, blank=True)
    cancel_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = " Transactions"
        ordering = ['-id']

    def __str__(self):
        return f"{self.id}: {self.transaction_id}"








