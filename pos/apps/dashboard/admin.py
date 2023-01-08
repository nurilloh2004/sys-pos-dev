from django.contrib import admin
from .models import Currency, Category, UserRole, SelectedPermission


@admin.register(Currency)
class Admin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "value",
    ]
    list_display_links = ('name', 'value')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "parent",
        "path",
        "slug",
        "status",
        "created_at"
    ]
    list_filter = ("parent",)
    list_display_links = ("name", "parent")
    search_fields = ('name',)


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "group",
        "creator",
        "user",
        "created_at"
    ]
    list_filter = ("created_at",)
    list_display_links = ("name", "user")
    search_fields = ('name',)


@admin.register(SelectedPermission)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "permission",
        "created_at"
    ]
    list_filter = ("created_at",)
    list_display_links = ("name", "permission")
