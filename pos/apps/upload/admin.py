from django.contrib import admin
from .models import UploadFile, OutletImage, BaseProductImage, OutletProductImage, UserProfileImage


@admin.register(UploadFile)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "file",
        "url",
    ]
    list_display_links = ("file", "url")


@admin.register(OutletImage)
class ModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "outlet",
        "image",
    ]
    list_display_links = ("outlet",)


@admin.register(BaseProductImage)
class ModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "instance",
        "image_id",
        "image",
    ]
    list_display_links = ("instance",)


@admin.register(OutletProductImage)
class ModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "instance",
        "image_id",
        "image",
    ]
    list_display_links = ("instance",)


@admin.register(UserProfileImage)
class ModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "instance",
        "image_id",
        "image",
    ]
    list_display_links = ("instance",)
