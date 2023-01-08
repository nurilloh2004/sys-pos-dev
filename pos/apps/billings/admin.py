from django.contrib import admin
from .models import BillingAccount, UserBalance, Transfer, Transaction


@admin.register(BillingAccount)
class ModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user_id",
        "user",
        "type",
    ]
    list_filter = ("created_at", "type")
    list_display_links = ("id", "user")


@admin.register(UserBalance)
class ModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "amount",
        "is_blocked",
    ]
    list_filter = ("created_at",)
    list_display_links = ("user", "amount")


@admin.register(Transfer)
class ModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "total",
        "currency",
        # "outlet",
    ]
    list_filter = ("created_at",)
    # list_display_links = ("outlet", "currency")


@admin.register(Transaction)
class ModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "transaction_id",
        "invoice",
        "origin",
        "destination",
        "pay_method",
        "reason",
        "amount",
        "status",
        "balance_updated"
    ]

    list_filter = ("created_at",)
    list_display_links = ("transaction_id", "invoice")



