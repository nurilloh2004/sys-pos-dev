from rest_framework import serializers
from apps.core.services.status import *
from .models import Currency, Category
from apps.dashboard.models import SelectedPermission


class SelectedPermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = SelectedPermission
        fields = ("id", "name")


class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = ('id', 'name', 'value')


class CategoryCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"
        # exclude = ["user", "slug"]


class SubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            'id',
            'parent',
            'name',
            'path',
            'slug',
        )


class CategorySerializer(serializers.ModelSerializer):
    children = SubCategorySerializer(many=True, required=False)

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'path',
            'slug',
            'children',
        )

    def validate_name(self, value):
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError("Category already exists!")
        return value

