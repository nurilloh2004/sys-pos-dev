from django.contrib import admin
from .models import Outlet, OutletCashBox, OutletMember, OutletCustomer
from apps.products.models import OutletProduct
from apps.address.models import Address, WorkingDay


class WorkingDayInline(admin.StackedInline):
    model = WorkingDay
    extra = 0


class AddressInline(admin.StackedInline):
    model = Address
    extra = 0


class OutletProductInline(admin.StackedInline):
    model = OutletProduct
    extra = 0


class MemberInline(admin.StackedInline):
    model = OutletMember
    extra = 0


@admin.register(OutletMember)
class Admin(admin.ModelAdmin):
    list_display = [
        "id",
        "user_id",
        "user",
        "outlet",
        "type",
        "outlet_type",
        "member_role",
        "status",
    ]
    list_filter = ("status", )
    list_display_links = ("user",)


@admin.register(OutletCustomer)
class Admin(admin.ModelAdmin):
    list_display = [
        "id",
        "user_id",
        "user",
        "outlet",
        "balance",
        "type",
        "status",
    ]
    list_filter = ("status", "type")
    list_display_links = ("user",)


@admin.register(Outlet)
class OutletAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "type",
        "owner",
        "user",
        "parent",
        "name",
        "legal_name",
        "phone",
        "currency",
        "status"
    ]
    list_filter = ("user", "type", 'status', "id",
        "type",
        "owner",
        "user",
        "parent",
        "name",)
    list_display_links = ("user", "name",)
    inlines = [AddressInline, OutletProductInline, MemberInline, WorkingDayInline]
    search_fields = ['id', 'name', 'legal_name', 'phone', 'user__email', 'user__phone']


@admin.register(OutletCashBox)
class OutletAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "outlet",
        "name",
        "balance",
        "currency"
    ]
    list_filter = ("created_at",)
    list_display_links = ("name", "outlet",)








