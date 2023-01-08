from django.contrib import admin
from .models import Region, District, Address, WorkingDay


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
    ]
    list_display_links = ('name', )


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "region",
        "status",
    ]
    list_filter = ("region", "status")
    list_display_links = ('name', )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "address1",
        "region",
        "district",
        "type",
        "status"
    ]
    list_filter = ("region", "status")
    list_display_links = ('id', 'address1', 'region', 'district')


@admin.register(WorkingDay)
class WorkingDayAdmin(admin.ModelAdmin):
    list_display = ['id', 'shop', 'is_working_day', 'day', 'work_start', 'work_end', 'created_at', 'updated_at']
    list_filter = ('shop__name',)
    list_display_links = ("shop",)
