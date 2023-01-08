from apps.core.models import TimestampedModel
from apps.core.services.status import *
from apps.outlets.models import Outlet


class Region(TimestampedModel):
    name = models.CharField(max_length=256)

    class Meta:
        verbose_name_plural = "Regions"
        ordering = ['-id']

    def __str__(self):
        return self.name


class District(TimestampedModel):
    name = models.CharField(max_length=256)
    region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name="district")
    status = models.IntegerField(choices=DistrictStatus.choices, default=DistrictStatus.ACTIVE)

    class Meta:
        verbose_name_plural = "Districts"
        ordering = ['-id']

    def __str__(self):
        return self.name


class Address(TimestampedModel):
    address1 = models.CharField(max_length=255, blank=True)
    address2 = models.CharField(max_length=255, blank=True)
    latitude = models.CharField(max_length=20, default="41.123456")
    longitude = models.CharField(max_length=20, default="71.123456")
    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE, related_name="shop_address")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="region_outlet", null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name="district_outlet", null=True)
    type = models.IntegerField(choices=AddressType.choices, default=AddressType.DROP)
    status = models.IntegerField(choices=BaseStatus.choices, default=BaseStatus.DEFAULT)

    class Meta:
        verbose_name_plural = "Addresses"
        ordering = ['-id']

    def __str__(self):
        if self.region:
            title = self.region.name
        else:
            title = self.address1
        return title

    def model_create(self, name, outlet_id):
        return self.objects.create(address1=name, outlet_id=outlet_id)


class WorkingDay(TimestampedModel):
    class AddressWorkingDay(models.IntegerChoices):
        MONDAY = 1
        TUESDAY = 2
        WEDNESDAY = 3
        THURSDAY = 4
        FRIDAY = 5
        SATURDAY = 6
        SUNDAY = 7

    shop = models.ForeignKey(Outlet, on_delete=models.CASCADE, related_name="working_day")
    is_working_day = models.BooleanField(default=True)
    day = models.IntegerField(choices=AddressWorkingDay.choices)
    work_start = models.TimeField()
    work_end = models.TimeField()

    def __str__(self):
        return f"Outlet ID : {self.shop.id}"

    class Meta:
        verbose_name_plural = "WorkingDays"
        ordering = ['id']

