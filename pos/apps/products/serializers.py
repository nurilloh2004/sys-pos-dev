from rest_framework import serializers
from apps.core.services.status import *
from apps.products.models import OutletProduct
from apps.dashboard.serializers import CategorySerializer
from .models import Attribute, AttributeValue, Brand, Measurement, BaseProduct, InternationProduct


class AttributeValueSerializer(serializers.ModelSerializer):
    attribute = serializers.CharField(source='attribute.name', read_only=True)
    name = serializers.CharField(source='value')

    class Meta:
        model = AttributeValue
        fields = ('id', 'attribute', 'name')


class AttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attribute
        fields = ('id', 'name')

    def to_representation(self, instance: Attribute):
        data = super(AttributeSerializer, self).to_representation(instance=instance)
        qs = AttributeValue.objects.filter(attribute_id=instance.id)
        if qs.exists():
            data["attributes"] = AttributeValueSerializer(qs, many=True).data
        else:
            data["attributes"] = []
        return data


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ('id', 'name')


class MeasurementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Measurement
        fields = ('id', 'name')


class OutletProductSerializer(serializers.ModelSerializer):
    attributes = AttributeValueSerializer(read_only=True, many=True)

    class Meta:
        model = OutletProduct
        fields = (
            'id',
            'px_code',
            'prod_code',
            'original_price',
            'selling_price',
            'minimal_price',
            'attributes'
        )


class CreateBaseProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = BaseProduct
        fields = (
            'id',
            'title',
            'brand',
            'category',
            'unit',
            'description',
            'upc',
            'photos'
        )

    def to_representation(self, instance: BaseProduct):
        data = super(CreateBaseProductSerializer, self).to_representation(instance=instance)
        qs = OutletProduct.objects.filter(product_id=instance.id)
        data["variations"] = OutletProductSerializer(qs, many=True).data
        data["images"] = instance.images
        return data


class BaseProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    category = CategorySerializer()
    unit = MeasurementSerializer()

    class Meta:
        model = BaseProduct
        fields = (
            'id',
            'title',
            'brand',
            'category',
            'unit',
            'description',
            'upc',
            'images',
        )

    def to_representation(self, instance: BaseProduct):
        data = super(BaseProductSerializer, self).to_representation(instance=instance)
        qs = OutletProduct.objects.filter(product_id=instance.id)
        data["variations"] = OutletProductSerializer(qs, many=True).data
        return data


class BaseProductListSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    category = CategorySerializer()
    unit = MeasurementSerializer()

    class Meta:
        model = BaseProduct
        fields = (
            'id',
            'title',
            'brand',
            'category',
            'unit',
            'description',
            'status',
            'images',
        )

    def to_representation(self, instance: BaseProduct):
        data = super(BaseProductListSerializer, self).to_representation(instance=instance)
        qs = OutletProduct.objects.filter(product_id=instance.id)
        price = float(0.0)
        if qs.exists():
            price = qs.last().original_price
        data["price"] = price
        data["variation_count"] = qs.count()
        return data


class InternationProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = InternationProduct
        fields = (
            'barcode_number',
            'barcode_formats',
            'mpn',
            'model',
            'asin',
            'title',
            'category',
            'last_child',
            'manufacturer',
            'brand',
            'ingredients',
            'nutrition_facts',
            'color',
            'gender',
            'material',
            'pattern',
            'size',
            'length',
            'width',
            'height',
            'weight',
            'release_date',
            'description',
            'images',
        )
