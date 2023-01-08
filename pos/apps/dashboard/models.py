from django.contrib.auth.models import ContentType
from apps.core.models import TimestampedModel
from django.contrib.auth.models import (
    AbstractBaseUser,
    Group,
    PermissionsMixin,
    Permission,
)
from apps.core.services.status import *


class Currency(TimestampedModel):
    name = models.CharField(max_length=5)
    value = models.CharField(max_length=256, default="0", blank=True)
    status = models.IntegerField(choices=BaseStatus.choices, default=BaseStatus.ACTIVE)

    class Meta:
        verbose_name_plural = "Currencies"
        ordering = ['-id']

    def __str__(self):
        return self.name

    @classmethod
    def get_currency_uzs(cls):
        obj, _ = cls.objects.get_or_create(name="UZS", value="10900")
        return obj

    @classmethod
    def get_currency_usd(cls):
        obj, _ = cls.objects.get_or_create(name="USD", value="1")
        return obj


class Category(TimestampedModel):
    parent = models.ForeignKey('self', related_name='children', on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=255, unique=True)
    path = models.TextField(null=True, blank=True)
    status = models.IntegerField(choices=BaseStatus.choices, default=BaseStatus.ACTIVE)
    slug = models.SlugField(max_length=255, blank=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['-id']

    @classmethod
    def get_telephone(cls, name):
        parent, _ = Category.objects.get_or_create(name="Electronics")
        qs = Category.objects.filter(parent_id=parent.id, name__iexact=name)
        if qs.exists():
            return qs.last()
        else:
            return Category.objects.create(parent_id=parent.id, name=name)


class SelectedPermission(TimestampedModel):
    name = models.CharField(max_length=255, blank=True)
    permission = models.ForeignKey(Permission, models.CASCADE)

    class Meta:
        verbose_name_plural = "SelectedPermission"
        ordering = ['id']

    def __str__(self):
        return self.name


class UserRole(TimestampedModel):
    name = models.CharField(max_length=150)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    creator = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name='role_owner')
    user = models.OneToOneField("accounts.User", on_delete=models.CASCADE, related_name='user_role', null=True, blank=True)
    permission_ids = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = "Roles"
        ordering = ['-id']

    def __str__(self):
        return self.name

    @property
    def permissions(self):
        data = []
        for permission_id in self.permission_ids.split(","):
            try:
                item = SelectedPermission.objects.get(id=int(permission_id))
                data.append({"id": item.id, "name": item.name})
            except SelectedPermission.DoesNotExist:
                continue
        return data
