from rest_framework.permissions import IsAuthenticated
from .models import OutletProduct
from apps.products.models import Brand, Attribute, AttributeValue, BaseProduct, Measurement
from apps.core.services.generics import CustomCreateUpdateView, CustomModelViewSet, CustomListView, \
    CustomGenericAPIView
from apps.core.services.status import *
from .utils.services import ProductController
from apps.core.services.generics import POSResponse
from apps.outlets.utils.services import OutletController
from . import serializers as ser


class AttributeAddView(CustomGenericAPIView):
    serializer_class = ser.AttributeValueSerializer
    permission_classes = [IsAuthenticated]
    tags = ["Add new attributes API"]

    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            attr = Attribute.objects.get(id=data['parent'])
            if AttributeValue.objects.filter(attribute_id=attr.id, value__iexact=data['name']).exists():
                self.update_error_text(catch=data['name'])
                self.code = POSResponse.CODE_1
                self.error_message = POSResponse.MSG_1
                return self.error_response()
            value = AttributeValue.objects.create(attribute_id=attr.id, value=self.capitalize(data['name']))
            serializer = self.serializer_class(instance=value)
            return self.success_response(results=serializer.data)
        except Exception as e:
            self.code = POSResponse.CODE_3
            self.error_message = POSResponse.MSG_3
            self.exception = e.args
            return self.error_response()


class AttributeViewSet(CustomModelViewSet):
    """
    POST: {"name": "Size", "attribute": ["S", "M", "L"]}
    """

    serializer_class = ser.AttributeSerializer
    queryset = Attribute.objects.filter(status=BaseStatus.ACTIVE)
    model = Attribute
    permission_classes = [IsAuthenticated]
    tags = ["Attributes API"]

    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            attribute, created = Attribute.objects.get_or_create(name=self.capitalize(data["parent"]))
            val, _ = AttributeValue.objects.get_or_create(
                attribute_id=attribute.id, value=self.capitalize(data["name"])
            )
            serializer = self.serializer_class(attribute)
            return self.success_response(results=serializer.data)
        except Exception as e:
            self.code = POSResponse.CODE_3
            self.error_message = POSResponse.MSG_3
            self.exception = e.args
            return self.error_response()

    def update(self, request, *args, **kwargs):
        data = request.data
        try:
            if "parent" in data and data["parent"]:
                attr = Attribute.objects.get(id=self.kwargs["pk"])
                attr.update(name=data['parent'])
            instance = AttributeValue.objects.get(id=data['id'])
            instance.update(value=data['name'])
            return self.success_response(results=instance.to_dict())
        except Exception as e:
            self.code = POSResponse.CODE_3
            self.error_message = POSResponse.MSG_3
            self.exception = e.args
            return self.error_response()

    def save_attr_value(self, attribute: Attribute, is_created: bool):
        data = self.request.data
        if is_created:
            for attr in list(data["attribute"]):
                AttributeValue.objects.create(attribute_id=attribute.id, value=attr)
        else:
            for attr in list(data["attribute"]):
                val, _ = AttributeValue.objects.get_or_create(attribute_id=attribute.id, value=attr)


class UnitViewSet(CustomModelViewSet):
    tags = ["Measurement API"]
    serializer_class = ser.MeasurementSerializer
    queryset = Measurement.objects.filter(status=BaseStatus.ACTIVE)
    model = Measurement


class UnitViewSet2(CustomModelViewSet):
    tags = ["Measurement API"]
    serializer_class = ser.MeasurementSerializer
    queryset = Measurement.objects.filter(status=BaseStatus.ACTIVE)
    model = Measurement


class BrandViewSet(CustomModelViewSet):
    tags = ["Brand API"]
    serializer_class = ser.BrandSerializer
    queryset = Brand.objects.filter(status=BaseStatus.ACTIVE)
    model = Brand


class ProductViewSet(CustomCreateUpdateView, OutletController):
    queryset = BaseProduct.objects.all()
    serializer_class = ser.BaseProductSerializer
    permission_classes = [IsAuthenticated]
    model = BaseProduct
    tags = ["Product API"]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        data = request.data
        return self.custom_update(data=data, partial=partial)

    def create(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        required = ["title", "category", "brand", "upc"]
        for item in required:
            if item not in data:
                self.code = POSResponse.CODE_20
                self.error_message = POSResponse.MSG_20
                self.update_error_text(catch=item)
                return self.error_response()

        if data["pay_type"] not in [InvoiceReceiptType.CASH, InvoiceReceiptType.CARD, InvoiceReceiptType.CREDIT]:
            raise CustomValidationError(debug=data["pay_type"])

        images = None
        if "images" in data and data["images"]:
            data['photos'] = data['images']
        #     self.validator_images()
        #     images = data["images"]

        if isinstance(data["brand"], str):
            data["brand"] = self.get_brand_by_name(name=data["brand"]).id

        if isinstance(data["category"], str):
            data["category"] = self.get_category_by_name().id

        if "unit" not in data:
            data["unit"] = self.get_default_unit().id

        if "variations" not in data:
            data["variations"] = [self.get_default_variation()]

        for variation in data["variations"]:
            if "images" in variation and variation["images"]:
                self.validator_images(images_list=variation["images"])

        provider = self.get_provider_by_id()  # Billing Account
        payer = self.get_payer_by_id()  # Billing Account

        outlet = self.get_user_main_shop()
        variations = data.pop("variations")
        # if self.validate_attributes(attributes=variations) is False:
        #     self.code = POSResponse.CODE_17
        #     self.error_message = POSResponse.MSG_17
        #     return self.error_response()

        if "parent" in data and data["parent"]:
            # add product variations
            base = BaseProduct.objects.get(id=data["parent"])
        else:
            # create new base product then add variations
            serializer = ser.CreateBaseProductSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            base = serializer.instance

        prices = {
            "original": data.get("original_price", 0),
            "selling": data.get("selling_price", 0),
            "minimal": data.get("minimal_price", 0)
        }
        color = data['color']
        memory = data['memory']

        variation_count = 0

        for var in variations:
            variation_count += 1
            # NOTE: barcode > IMEI
            # // Save product to this marketplace
            product = outlet.create_market_product(
                user_id=user.id,
                product_id=base.id,
                prod_code=var["barcode"],
                qty=var["quantity"],
                color=color,
                memory=memory,
                prices=prices
            )

            # self.product_income(outlet_id=outlet.id, product_id=product.id, qty=var["quantity"])

            # provider = outlet.owner.private_buyer_bln()  # поставщик товара
            # buyer = outlet.owner.get_billing_user(user_id=outlet.owner.id)  # покупатель (outlet/shop)

            self.track_product(
                product=product,
                action_type=InOutType.BUYING,
                pay_type=data['pay_type'],
                provider_id=provider.id,
                quantity=1
            )

            if "images" in var:
                product.add_variation_images(images=var['images'])

        amount = int(prices.get("original")) * variation_count
        if data['pay_type'] == InvoiceReceiptType.CREDIT:
            self.update_cash_box(shop=outlet, minus=amount)

        self.create_transaction(
            origin=payer,
            dest=provider.user.get_billing_user(user_id=provider.user_id),
            pay_method=PaymentMethod.CASH,
            reason=TransactionReason.DEBIT,
            amount=amount
        )

        serializer = self.serializer_class(instance=base)
        return self.success_response(results=serializer.data)


class OutletProductViewSet(CustomCreateUpdateView):
    queryset = OutletProduct.objects.all()
    serializer_class = ser.OutletProductSerializer
    permission_classes = [IsAuthenticated]
    model = OutletProduct
    tags = ["Product variation API"]

    def update(self, request, *args, **kwargs):

        partial = kwargs.pop('partial', False)
        instance = self.get_instance()
        data = request.data
        is_images = False

        if "images" in data and data["images"]:
            self.validator_images()
            is_images = True

        if "attributes" in data and data["attributes"]:
            instance.update_attributes(attributes=data["attributes"])

        if is_images:
            instance.add_variation_images(images=data["images"])

        serializer = self.serializer_class(instance=instance, data=data, partial=partial)

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return self.success_response(results=serializer.data)


class IncomeProductView(CustomGenericAPIView, OutletController):
    serializer_class = ser.BaseProductSerializer
    permission_classes = [IsAuthenticated, ]
    tags = ["Income product API"]

    def post(self, request, *args, **kwargs):
        data = request.data
        qs = BaseProduct.objects.filter(id=data["parent"])
        if not qs.exists():
            self.update_error_text(catch=data["parent"])
            self.code = POSResponse.CODE_4
            self.error_message = POSResponse.MSG_4
            return self.error_response()

        if ("variations" not in data) or ("parent" not in data):
            self.code = POSResponse.CODE_16
            self.error_message = POSResponse.MSG_16
            self.update_error_text(catch=["variations | parent"])
            return self.error_response()

        serializer = self.serializer_class(instance=qs.last())
        return self.success_response(results=serializer.data)


class ProductListView(CustomListView):
    queryset = BaseProduct.objects.filter(status=BaseProductStatus.ACTIVE)
    serializer_class = ser.BaseProductListSerializer
    permission_classes = [IsAuthenticated]
    tags = ["Product list API"]


class AttributeViewList(CustomListView):
    serializer_class = ser.AttributeSerializer
    permission_classes = [IsAuthenticated]
    tags = ["Attributes list API"]

    def get_queryset(self):
        return Attribute.objects.filter(status=BaseStatus.ACTIVE)



