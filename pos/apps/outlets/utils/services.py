from apps.core.services.generics import POSResponse
from apps.core.services.status import *
from apps.core.services.controller import Controller
from apps.outlets.models import User
from apps.outlets.models import OutletCustomer, OutletMember
from apps.products.models import OutletProduct
from apps.address.models import Address
from apps.billings.utils.services import TransactionController


class OutletController(TransactionController):

    def shop_working_day(self, shop):
        data = self.request.data
        if "working_hours" in data and data["working_hours"]:
            self.create_working_day(shop=shop, working_hours=data["working_hours"])

    def create_shop_address(self, shop, region_id, district_id):
        data = self.request.data
        address2 = ""
        if "address2" in data and data["address2"]:
            address2 = data["address2"]

        try:
            Address(
                address1=data["address_name"],
                address2=address2,
                latitude=data["latitude"],
                longitude=data["longitude"],
                outlet_id=shop.id,
                region_id=region_id,
                district_id=district_id,
            ).save()
        except Exception as e:
            raise CustomValidationError(debug=str(e.args))

    def update_cash_box(self, shop, plus=None, minus=None):
        """
        en: Add or subtract from OutletCashBox > balance
        ru: Добавить или вычесть из баланса магазина
        """
        cash_box = shop.get_shop_cash()
        if plus and minus is None:
            cash_box.balance += plus
        if minus and plus is None:
            cash_box.balance -= minus
        cash_box.save()
        self.reporter(message=f"Баланс касса: {cash_box.balance}")
        return cash_box

    def update_quantity_in_market(self, invoice):
        for product in invoice.products.all():
            print("update_quantity_in_market .....", product, type(product))
            OutletProduct.objects.filter(id=product.id).update(quantity=F('quantity') - 1)

    def get_provider_by_id(self):
        """ Get provider by ID """
        provider = self.request.data.get("provider", None)
        if provider:
            qs = OutletCustomer.objects.filter(id=provider, type=OutletCustomerType.PROVIDER)
            if qs.exists():
                return qs.last()
            else:
                raise CustomValidationError(debug="Invalid provider")
        else:
            raise CustomValidationError(debug="Invalid provider")

    def get_payer_by_id(self):
        """
        Find owner member by ID if exists. `Робот покупатель` otherwise
        """
        data = self.request.data

        if data.get("payer", None):
            qs = OutletMember.objects.filter(id=data["payer"], type=OutletMemberType.OWNER)
            if qs.exists():
                owner = qs.last()

                payer = owner.user.get_billing_user(user_id=owner.user_id)
            else:
                raise CustomValidationError(debug="Invalid payer")
        else:
            payer = User.private_buyer_bln()  # Робот покупатель для частных (private) пользователей
        return payer


class CheckoutController(Controller):

    def validate_payment_type(self):
        """
        InvoiceReceiptType.CASH = 1
        InvoiceReceiptType.CARD = 2
        InvoiceReceiptType.CASH_CARD = 4
        InvoiceReceiptType.CREDIT = 8
        """
        data = self.request.data

        amount_cash = float(0.0)
        amount_card = float(0.0)

        pay_type = data['pay_type']

        if pay_type in [1, 2, 4, 8]:
            if pay_type == InvoiceReceiptType.CASH_CARD:
                if not data["cash"] or not data["card"]:
                    raise CustomValidationError(debug=pay_type)

                amount_cash = int(data["cash"])
                amount_card = int(data["card"])

            elif pay_type == InvoiceReceiptType.CREDIT:
                if not data["client"]:
                    raise CustomValidationError(debug=pay_type)

            return pay_type, amount_cash, amount_card
        else:
            raise CustomValidationError(debug=pay_type)

    def get_buyer_by_id(self):
        """
        Find user by ID if exists. `Робот покупатель` otherwise
        """
        data = self.request.data

        if data.get("client", None):
            qs = OutletCustomer.objects.filter(id=data["client"], type=OutletCustomerType.CLIENT)
            if qs.exists():
                client = qs.last()

                buyer = client.user.get_billing_user(user_id=client.user_id)
            else:
                raise CustomValidationError(debug="Invalid client")
        else:
            buyer = User.private_buyer_bln()  # Робот покупатель для частных (private) пользователей
        return buyer
#
# try:
#     q = OutletProduct.objects.filter(outlet_id=1).aggregate(all_count=Sum('quantity'))['all_count']
#     print("Q......", q)
# except Exception as e:
#     print("EEE>.......", e.args)