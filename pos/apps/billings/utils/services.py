from apps.core.services.status import *
from apps.core.services.controller import Controller
from ..models import Transaction
from apps.products.models import InOutProduct


class BillingController(Controller):
    pass


class TransactionController(Controller):

    def create_transaction(self, origin, dest, pay_method: PaymentMethod, reason: TransactionReason, amount, invoice=None):
        """
        invoice,
        origin > buyer/client (покупатель),
        dest > receiver/recipient (получатель),
        pay_method,
        reason,
        amount
        """
        try:
            Transaction.objects.create(
                invoice=invoice,
                origin=origin,
                destination=dest,
                pay_method=pay_method,
                reason=reason,
                amount=amount
            )
        except Exception as e:
            self.log(message=str(e.args))

    def track_product(self, product, action_type, pay_type, provider_id=None, client_id=None, quantity=1):
        try:
            InOutProduct.objects.create(
                outlet_id=product.outlet.id,
                product_id=product.id,
                provider_id=provider_id,
                client_id=client_id,
                quantity=quantity,
                pay_type=pay_type,
                type=action_type
            )
        except Exception as e:
            self.log(message=str(e.args))
