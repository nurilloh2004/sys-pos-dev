from apps.core.models import TimestampedModel
from apps.accounts.models import User
from apps.core.services.status import *
from apps.dashboard.models import Currency
from apps.billings.models import UserBalance


class Outlet(TimestampedModel):
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="outlet_owner", blank=True, null=True)

    # update to current login user for BRANCH SHOP
    # user > cashier
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="outlet_user", blank=True, null=True)

    parent = models.ForeignKey('self', related_name='children', on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=255)
    legal_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(default="dts@gmail.com")
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, blank=True, null=True)
    type = models.IntegerField(choices=OutletType.choices, default=OutletType.BRANCH)
    status = models.IntegerField(choices=OutletStatus.choices, default=OutletStatus.ACTIVE)

    class Meta:
        verbose_name_plural = "  Outlets"
        ordering = ['-id']

    def __str__(self):
        return f"{self.id}: {self.name}"

    def get_shop_cash(self):
        return self.shop_cash_box

    @property
    def shop_cash(self):
        cash_box = self.shop_cash_box
        return {
            "id": cash_box.id,
            "name": cash_box.name,
            "balance": cash_box.balance
        }

    def add_outlet_image(self, images: list):
        for image_id in images:
            if not self.outlet_image.filter(outlet_id=self.id, image_id=image_id).exists():
                self.outlet_image.create(outlet_id=self.id, image_id=image_id)

    @property
    def images(self):
        qs = self.outlet_image.filter(outlet_id=self.id, status=BaseStatus.DEFAULT)
        # qs = OutletImage.objects.filter(outlet_id=self.id, status=BaseStatus.DEFAULT)
        data = []
        if qs.exists():
            instance = qs.latest('created_at')
            data.append({"id": instance.image.id, "url": instance.image.url})
        return data

    # def save(self, *args, **kwargs):
    #     super(Outlet, self).save(*args, **kwargs)

    def update_address(self, **kwargs: dict):
        qs = self.shop_address.filter(outlet_id=self.id)
        if qs.exists():
            obj = qs.last()
            data = {
                "address1": kwargs.get('address_name', obj.address1),
                "address2": kwargs.get('address2', obj.address2),
                "latitude": kwargs.get('latitude', obj.latitude),
                "longitude": kwargs.get('longitude', obj.longitude),
                "region_id": "",
                "district_id": "",
            }
            region = kwargs.get('region', None)
            district = kwargs.get('district', None)
            if region:
                data['region_id'] = region

            if district:
                data['district_id'] = district
            qs.update(**data)

    def create_outlet_member(self, user_id=None):
        if user_id is None:
            user_id = self.user_id
        self.outlet_member.create(user_id=user_id, outlet_id=self.id, status=BaseStatus.ACTIVE)

    def create_outlet_customer(self, user_id=None, customer_type=OutletCustomerType.CLIENT):
        if user_id is None:
            user_id = self.user_id
        customer = self.customer_user.create(user_id=user_id, outlet_id=self.id, type=customer_type)
        return customer

    def save_working_day(self, item):
        self.working_day.model(
            shop_id=self.id,
            is_working_day=item["status"],
            day=item["day"],
            work_start=item["start"],
            work_end=item["end"]
        ).save()

    def get_work_mode(self):
        qs_work_time = self.working_day.order_by('day')
        working_hours = []
        if qs_work_time.exists():
            for item in qs_work_time:
                status = 1 if item.is_working_day else 0
                working_hours.append(
                    {
                        "id": item.id,
                        "day": item.day,
                        "name": self.WEEKS.get(item.day, "null"),
                        "start": item.work_start.strftime("%H:%M"),
                        "end": item.work_end.strftime("%H:%M"),
                        "status": status
                    }
                )
        return working_hours

    def get_address(self):
        qs = self.shop_address.filter(status=BaseStatus.DEFAULT)
        if qs.exists():
            address = qs.last()
        else:
            address = self.shop_address.create(address1=self.name, outlet_id=self.id)
        return address

    def create_market_product(self, user_id: int, product_id: int, prod_code: str, qty: int, color, memory, prices):
        """
        Add this product to current Marketplace
        Create new `Variation` if not exists... then save new attributes
        """
        product = self.marketplace_product.filter(
            user_id=user_id, product_id=product_id, prod_code=prod_code, outlet_id=self.id
        )

        if product.exists():
            return product.last()

        else:
            new_product = self.marketplace_product.create(
                user_id=user_id,
                outlet_id=self.id,
                product_id=product_id,
                prod_code=prod_code,
                original_price=prices.get("original", float(0.0)),
                selling_price=prices.get("selling", float(0.0)),
                minimal_price=prices.get("minimal", float(0.0)),
                quantity=qty
            )
            if color:
                new_product.set_color(val=color)
            if memory:
                new_product.set_memory(val=memory)
            return new_product

    @property
    def address(self):
        """ Get outlet address """
        qs = self.shop_address.filter(status=BaseStatus.DEFAULT)
        if qs.exists():
            instance = qs.last()
            data = {
                "id": instance.id,
                "address1": instance.address1,
                "address2": instance.address2,
                "latitude": instance.latitude,
                "longitude": instance.longitude,
                "region": {"id": instance.region.id, "name": instance.region.name},
                "district": {"id": instance.district.id, "name": instance.district.name}
            }
        else:
            data = None
        return data

    @property
    def coworkers(self):
        """ Get outlet worker """
        qs = self.outlet_member.filter(status=BaseStatus.ACTIVE).exclude(user_id=self.owner_id)
        results = []
        if qs.exists():
            for worker in qs.all():
                results.append({
                    "user_id": worker.user.id,
                    "member_id": worker.id,
                    "username": worker.user.username,
                    "first_name": worker.user.first_name,
                    "last_name": worker.user.last_name,
                    "fullname": worker.user.fullname,
                    "phone": worker.user.phone,
                    "role": worker.user.get_model_permissions(),
                })
        return results


class OutletCashBox(TimestampedModel):
    """ касса магазина """
    outlet = models.OneToOneField(Outlet, on_delete=models.PROTECT, related_name="shop_cash_box")
    name = models.CharField(max_length=255)
    balance = models.DecimalField(default=0.0, max_digits=15, decimal_places=2)
    currency = models.IntegerField(choices=CurrencyType.choices, default=CurrencyType.UZS)
    status = models.IntegerField(choices=BaseStatus.choices, default=BaseStatus.DEFAULT)

    class Meta:
        verbose_name_plural = "OutletCashBox"
        ordering = ['id']

    def __str__(self):
        return f"CashBox: {self.id}: {self.balance}"


class OutletMember(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="member")
    outlet = models.ForeignKey(Outlet, on_delete=models.PROTECT, related_name="outlet_member")
    type = models.IntegerField(choices=OutletMemberType.choices, default=OutletMemberType.MEMBER)
    status = models.IntegerField(choices=BaseStatus.choices, default=BaseStatus.ACTIVE)

    class Meta:
        verbose_name_plural = " OutletMembers"
        ordering = ['-id']

    def __str__(self):
        return f"{self.user.phone} / {self.outlet.name}"

    @property
    def role(self):
        return self.user.get_model_permissions()

    def member_role(self):
        return self.user.groups.name if self.user.groups else "-"

    def outlet_type(self):
        return self.outlet.get_status_display()

    @property
    def type_display(self):
        return self.get_type_display()


class OutletCustomer(TimestampedModel):
    """ Provide | Client """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer")
    outlet = models.ForeignKey(Outlet, on_delete=models.PROTECT, related_name="customer_user")
    balance = models.ForeignKey(UserBalance, on_delete=models.PROTECT, related_name="customer_balance", null=True, blank=True)
    type = models.IntegerField(choices=OutletCustomerType.choices, default=OutletCustomerType.CLIENT)
    status = models.IntegerField(choices=BaseStatus.choices, default=BaseStatus.ACTIVE)

    class Meta:
        verbose_name_plural = " OutletCustomers"
        ordering = ['-id']

    def __str__(self):
        return f"{self.user.phone}"

    def images(self):
        """ Customer images """
        return self.user.images




