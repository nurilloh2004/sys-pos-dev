import os
from django.core.files import File
from apps.core.models import TimestampedModel
from apps.core.services.status import *
from apps.outlets.models import User, Outlet
from apps.products.models import BaseProduct, OutletProduct
from django.core import files
import urllib.request


class UploadFile(TimestampedModel):
    file = models.FileField(upload_to='upload/file/')

    def __str__(self):
        return f"{self.file}"

    @property
    def url(self):
        if self.file:
            # path = f"{settings.BASE_URL}{self.file.url}"
            path = f"https://posox.site.uz{self.file.url}"
        else:
            path = None
        return path

    class Meta:
        verbose_name_plural = "UploadFiles"
        ordering = ['-id']

    @classmethod
    def is_valid(cls, images):
        for image_id in images:
            try:
                cls.objects.get(id=image_id)
            except UploadFile.DoesNotExist:
                return False


class UploadImage(TimestampedModel):
    file = models.ImageField(upload_to='upload/image/')

    def __str__(self):
        return f"{self.file}"

    @property
    def url(self):
        if self.file:
            # path = f"{settings.BASE_URL}{self.file.url}"
            path = f"https://posox.site.uz{self.file.url}"
        else:
            path = None
        return path

    class Meta:
        verbose_name_plural = "UploadFiles"
        ordering = ['-id']


class OutletImage(TimestampedModel):
    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE, related_name="outlet_image")
    image = models.ForeignKey(UploadFile, on_delete=models.CASCADE)
    status = models.IntegerField(choices=BaseStatus.choices, default=BaseStatus.DEFAULT)

    def __str__(self):
        return f"Shop: {self.outlet.id} | File: {self.image.id}"

    class Meta:
        verbose_name_plural = "OutletImages"
        ordering = ['-id']


class BaseProductImage(TimestampedModel):
    url = models.CharField(max_length=500, blank=True)
    instance = models.ForeignKey(BaseProduct, on_delete=models.CASCADE, related_name="base_image")
    image = models.ForeignKey(UploadImage, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Base: {self.instance.id} | File: {self.image.id}"

    class Meta:
        verbose_name_plural = "BaseProductImages"
        ordering = ['-id']


# class ProductVariationImage(TimestampedModel):
#     instance = models.ForeignKey(ProductVariation, on_delete=models.CASCADE, related_name="variation_image")
#     image = models.ForeignKey(UploadFile, on_delete=models.CASCADE, null=True, blank=True)
#
#     def __str__(self):
#         return f"Variation: {self.instance.id} | File: {self.image.id}"
#
#     class Meta:
#         verbose_name_plural = "ProductVariationImages"
#         ordering = ['-id']


class OutletProductImage(TimestampedModel):
    instance = models.ForeignKey(OutletProduct, on_delete=models.CASCADE, related_name="variation_image")
    image = models.ForeignKey(UploadFile, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"OP-Variation: {self.instance.id} | File: {self.image.id}"

    class Meta:
        verbose_name_plural = "OutletProductImages"
        ordering = ['-id']


class UserProfileImage(TimestampedModel):
    instance = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile_image")
    image = models.ForeignKey(UploadFile, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"User: {self.instance.id} | File: {self.image.id}"

    class Meta:
        verbose_name_plural = "UserProfileImages"
        ordering = ['-id']

