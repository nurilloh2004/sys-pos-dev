from django.contrib import admin
from .models import (
    Attribute, AttributeValue, Brand, Measurement, BaseProduct, OutletProduct, InOutProduct, SalesProduct,
    InternationProduct
)


class VariationInline(admin.StackedInline):
    model = OutletProduct
    extra = 0


class AttributeValueInline(admin.StackedInline):
    model = AttributeValue
    extra = 0


@admin.register(Attribute)
class ModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "status",
    ]
    # list_filter = ("parent",)
    list_display_links = ("name", "status")
    inlines = [AttributeValueInline]


@admin.register(AttributeValue)
class ModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "attribute",
        "value",
        "status",
    ]


@admin.register(BaseProduct)
class ModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "brand",
        "category",
        "unit",
        "status",
    ]
    list_filter = ("created_at",)
    list_display_links = ("title", "brand", )
    inlines = [VariationInline]


@admin.register(OutletProduct)
class ModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "product",
        "title",
        "px_code",
        "prod_code",
        "original_price",
        "selling_price",
        "minimal_price",
        "quantity",
    ]
    filter_horizontal = ('attributes',)
    list_filter = ("created_at",)
    list_display_links = ("product", "px_code", "prod_code")


@admin.register(Brand)
class ModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "status",
    ]
    list_display_links = ("name",)


@admin.register(Measurement)
class ModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "status",
    ]
    list_display_links = ("name",)


@admin.register(InternationProduct)
class ModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "barcode_number",
        "model",
        "title",
        "category",
        "manufacturer",
        "brand",
    ]
    list_display_links = ("title",)


@admin.register(InOutProduct)
class ModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "outlet",
        "product",
        "provider",
        "client",
        "price",
        "quantity",
        "comment",
        "type",
    ]

    list_filter = ("type", "outlet", "provider", "client")
    list_display_links = ("outlet", "product")
    # search_fields = ('product',)


@admin.register(SalesProduct)
class ModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "outlet",
        "client",
        "product",
        "quantity",
    ]
