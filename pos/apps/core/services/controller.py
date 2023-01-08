from apps.core.notifications.pusher import TelegramPusher
from .status import *
from apps.core.exception.custom_exception import CustomValidationError
from apps.address.models import Region, District
from apps.address.models import WorkingDay
from apps.products.models import Attribute, AttributeValue


class Logging:

    @staticmethod
    def log(message: str):
        TelegramPusher(text=message).exception()

    @staticmethod
    def reporter(message: str):
        TelegramPusher(text=message).messenger()


class Controller(Logging):

    def __init__(self, request):
        self.request = request

    lookup_access_key: str = "access"
    lookup_refresh_key: str = "refresh"

    default_shop_name: str = "Основной"
    default_shop_legal_name: str = "OOO " + default_shop_name

    default_product_original_price = float(0.0)
    default_product_selling_price = float(0.0)
    default_product_minimal_price = float(0.0)
    default_product_quantity = 1

    OBJECT_ALREADY_EXISTS = "%s already exists"
    OBJECT_NOT_FOUND = "%s not found"

    currency = {"UZS": "11080", "USD": "1"}

    shop_days = [
        {
            "day": 1,
            "start": "08:00",
            "end": "20:00",
            "status": 1
        },
        {
            "day": 2,
            "start": "08:00",
            "end": "20:00",
            "status": 1
        },
        {
            "day": 3,
            "start": "08:00",
            "end": "20:00",
            "status": 1
        },
        {
            "day": 4,
            "start": "08:00",
            "end": "20:00",
            "status": 1
        },
        {
            "day": 5,
            "start": "08:00",
            "end": "20:00",
            "status": 1
        },
        {
            "day": 6,
            "start": "08:00",
            "end": "20:00",
            "status": 1
        },
        {
            "day": 7,
            "start": "00:00",
            "end": "00:00",
            "status": 0
        }
    ]

    def get_region(self):
        data = self.request.data
        if "region" in data and data["region"]:
            try:
                return Region.objects.get(id=data["region"]).id
            except Exception as e:
                raise CustomValidationError(debug=str(e.args))
        return None

    def get_district(self):
        data = self.request.data
        if "district" in data and data["district"]:
            try:
                return District.objects.get(id=data["district"]).id
            except Exception as e:
                raise CustomValidationError(debug=str(e.args))
        return None

    def create_working_day(self, shop, working_hours: list = None):
        if working_hours is None:
            for item in self.shop_days:
                shop.save_working_day(item=item)
        else:
            qs = WorkingDay.objects.filter(shop_id=shop.id)
            if qs.exists():
                qs.delete()
            for item in working_hours:
                shop.save_working_day(item=item)

    # def product_income(self, outlet_id, product_id, qty: int = 0, currency_id=None):
    #     """
    #     Income product variation
    #     outlet_id: outlet object ID
    #     product_id: base product ID
    #     variation: {}
    #     currency_id: optional
    #     """
    #     if currency_id is None:
    #         currency_id = Currency.get_currency_uzs().id
    #
    #     if qty == 0:
    #         qty = self.default_product_quantity
    #
    #     InOutProduct.objects.create(
    #         outlet_id=outlet_id,
    #         product_id=product_id,
    #         quantity=qty,
    #         currency_id=currency_id
    #     )

    def get_default_variation(self):
        """
        {
            "original_price": 950,
            "selling_price": 952,
            "minimal_price": 951,
            "quantity": 15,
            "attributes": [
                {
                    "name": 1, //Attribute ID
                    "value": 8  // AttributeValue ID
                }
            ]
        }
        """
        attr, _ = Attribute.objects.get_or_create(name="Color")
        qs = AttributeValue.objects.filter(attribute_id=attr.id, value="Black")
        if qs.exists():
            value = qs.last()
        else:
            value = AttributeValue.objects.create(attribute_id=attr.id, value="Black")
        return {
            "original_price": self.default_product_original_price,
            "selling_price": self.default_product_selling_price,
            "minimal_price": self.default_product_minimal_price,
            "quantity": self.default_product_quantity,
            "attributes": [value.serializer()]
        }

