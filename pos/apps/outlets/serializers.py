from rest_framework import serializers
from apps.core.services.status import *
from apps.accounts.serializers import UserDetailSerializer
from .models import Outlet, OutletMember, OutletCustomer, OutletCashBox
from apps.dashboard.serializers import CurrencySerializer, CategorySerializer
from apps.products.serializers import BrandSerializer, MeasurementSerializer, AttributeValueSerializer, OutletProductSerializer
from apps.products.models import OutletProduct, InOutProduct
from apps.billings.serializers import UserBalanceSerializer
from apps.address.serializers import Address, AddressMiniSerializer


class CreateOutletSerializer(serializers.ModelSerializer):
    ## region = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all(), allow_null=True, required=False)
    # district = serializers.PrimaryKeyRelatedField(queryset=District.objects.all(), allow_null=True)

    class Meta:
        model = Outlet
        fields = (
            "owner",
            "user",
            "parent",
            "name",
            "legal_name",
            "phone",
            "email",
            "currency",
        )


class OutletDetailSerializer(serializers.ModelSerializer):
    """ Outlet full serializers """
    owner = UserDetailSerializer()
    currency = CurrencySerializer()

    class Meta:
        model = Outlet
        fields = (
            "id",
            "owner",
            "parent",
            "name",
            "legal_name",
            "phone",
            "email",
            "address",
            "shop_cash",
            "currency",
            "coworkers",
            "images",
            "created_at",
        )

    def to_representation(self, instance: Outlet):
        data = super(OutletDetailSerializer, self).to_representation(instance=instance)
        data["working_days"] = instance.get_work_mode()
        in_store = OutletProduct.objects.filter(outlet_id=instance.id)

        date = datetime.now(tz=pytz.UTC)
        start_week = date - timedelta(date.weekday())
        end_week = start_week + timedelta(7)

        all_count = 0
        week_count = 0
        week_sell_sum = 0
        refund_product = 0

        if in_store.exists():
            for item in in_store:
                all_count += item.quantity

            for weekly in in_store.filter(created_at__range=[start_week, end_week]):
                week_count += weekly.quantity
                week_sell_sum += weekly.selling_price

        refunded = InOutProduct.objects.filter(outlet_id=instance.id, type=InOutType.REFUND)
        if refunded.exists():
            for item in refunded:
                refund_product += item.quantity

        data["progress"] = {
            "product_all_count": all_count,
            "product_week_count": week_count,
            "week_sell_sum": week_sell_sum,
            "refund_product_count": refund_product
        }
        return data


class OutletShortSerializer(serializers.ModelSerializer):
    """ Outlet short serializers """

    class Meta:
        model = Outlet
        fields = (
            "id",
            "name",
            "legal_name",
            "phone"
        )

    def to_representation(self, instance: Outlet):
        data = super(OutletShortSerializer, self).to_representation(instance=instance)
        qs = Address.objects.filter(outlet_id=instance.id)
        address = None
        if qs.exists():
            address = AddressMiniSerializer(instance=qs.last()).data

        data["address"] = address
        return data


class OutletMiniSerializer(serializers.ModelSerializer):
    """ Outlet mini serializers """

    class Meta:
        model = Outlet
        fields = (
            "id",
            "name",
            "legal_name",
            "phone"
        )


class OutletMemberDetailSerializer(serializers.ModelSerializer):
    """ OutletMember DETAIL SERIALIZERS """
    user_id = serializers.IntegerField(source='user.id')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    fullname = serializers.CharField(source='user.fullname')
    phone = serializers.CharField(source='user.phone')
    outlet = OutletShortSerializer()

    class Meta:
        model = OutletMember
        fields = (
            "id",
            "user_id",
            "first_name",
            "last_name",
            "fullname",
            "phone",
            "outlet",
            "role",
        )


class OutletMemberListSerializer(serializers.ModelSerializer):
    """ OutletMember LIST SERIALIZERS """
    user_id = serializers.IntegerField(source='user.id')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    name = serializers.CharField(source='user.name')
    phone = serializers.CharField(source='user.phone')
    outlet = OutletMiniSerializer()

    class Meta:
        model = OutletMember
        fields = (
            "id",
            "user_id",
            "first_name",
            "last_name",
            "name",
            "type_display",
            "phone",
            "outlet",
            "role",
        )


class OutletCustomerListSerializer(serializers.ModelSerializer):
    """ Должник / Поставщик """
    user_id = serializers.IntegerField(source='user.id')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    name = serializers.CharField(source='user.name')
    phone = serializers.CharField(source='user.phone')
    balance = UserBalanceSerializer()

    class Meta:
        model = OutletCustomer
        fields = (
            "id",
            "user_id",
            "first_name",
            "last_name",
            "name",
            "phone",
            "images",
            "balance",
        )


class OutletCustomerDetailSerializer(serializers.ModelSerializer):
    """ Клиент / Поставщик """
    user_id = serializers.IntegerField(source='user.id')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    name = serializers.CharField(source='user.name')
    phone = serializers.CharField(source='user.phone')
    balance = UserBalanceSerializer()

    class Meta:
        model = OutletCustomer
        fields = (
            "id",
            "user_id",
            "first_name",
            "last_name",
            "name",
            "phone",
            "images",
            "balance",
        )


class OutletCustomerHistorySerializer(serializers.ModelSerializer):
    """ History of customer """
    title = serializers.CharField(source='product.title')
    # brand = BrandSerializer(source='product.product.brand')
    category = CategorySerializer(source='product.product.category')
    unit = MeasurementSerializer(source='product.product.unit')
    px_code = serializers.CharField(source='product.px_code')
    prod_code = serializers.CharField(source='product.prod_code')
    currency = CurrencySerializer()

    class Meta:
        model = InOutProduct
        fields = (
            'id',
            'title',
            'category',
            'unit',
            'px_code',
            'prod_code',
            'px_code',
            'prod_code',
            'price',
            'quantity',
            'currency',
            'pay_type_display',
            'type_display',
        )


# Marketplace Product MODELSERIALIZER

class OutletProductsShortSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='product.title', read_only=True)
    selling_price = serializers.CharField(source='product.selling_price', read_only=True)

    class Meta:
        model = OutletProduct
        fields = (
            'id',
            'title',
            'tax_percent',
            'tax_amount',
            'selling_price'
        )


class ProductSearchSerializer(serializers.ModelSerializer):
    # title = serializers.CharField(source='product.title')

    class Meta:
        model = OutletProduct
        fields = (
            'id',
            'title',
            'prod_code',
            'selling_price',
            'quantity',
            'images',
        )


class SingleSearchSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='product.category.name')

    class Meta:
        model = OutletProduct
        fields = (
            'id',
            'title',
            'category',
            'px_code',
            'prod_code',
            'color',
            'memory',
            'original_price',
            'selling_price',
            'minimal_price',
            'quantity',
            'currency',
            'images'
        )


class ProductListSerializer(serializers.ModelSerializer):
    base_id = serializers.IntegerField(source='product.id')
    brand = BrandSerializer(source='product.brand')
    category = CategorySerializer(source='product.category')
    unit = MeasurementSerializer(source='product.unit')
    attributes = AttributeValueSerializer(read_only=True, many=True)
    title = serializers.CharField(source='product.title')
    currency = CurrencySerializer(source='outlet.currency')

    class Meta:
        model = OutletProduct
        fields = (
            'id',
            'base_id',
            'title',
            'brand',
            'category',
            'unit',
            'px_code',
            'prod_code',
            'attributes',
            'original_price',
            'selling_price',
            'minimal_price',
            'quantity',
            'status',
            'currency',
            'images',
        )


class ProductScannerSerializer(serializers.ModelSerializer):
    code = serializers.CharField(source='prod_code')

    class Meta:
        model = OutletProduct
        fields = ('code',)


class OutletCashBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutletCashBox
        fields = (
            'id',
            'name',
            'balance'
        )

