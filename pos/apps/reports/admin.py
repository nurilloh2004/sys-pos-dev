from django.contrib import admin
from .models import Invoice, InvoiceProduct, InvoiceReceipt, OutletExpense


@admin.register(Invoice)
class ModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "invoice_id",
        "seller",
        "buyer",
        "total",
        "status"
    ]

    filter_horizontal = ('products',)
    list_filter = ("created_at",)
    list_display_links = ("invoice_id",)


@admin.register(InvoiceProduct)
class ModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "count",
        "product",
        "invoice",
    ]

    list_filter = ("created_at",)
    list_display_links = ("product", "invoice")


@admin.register(InvoiceReceipt)
class ModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "invoice",
        "receipt_no",
        "pay_type",
        "amount_cash",
        "amount_card",
        "total",
        "status"
    ]

    list_filter = ("created_at", "pay_type")
    list_display_links = ("invoice", "pay_type")


@admin.register(OutletExpense)
class ModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "outlet",
        "amount",
        "currency"
    ]

    list_filter = ("created_at",)
    list_display_links = ("outlet", )