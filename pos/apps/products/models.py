from apps.core.models import TimestampedModel
from apps.core.services.status import *
from apps.accounts.models import User
from apps.outlets.models import Outlet, Currency, OutletCustomer
from apps.dashboard.models import Category
from .manager import ProductManager


class Attribute(TimestampedModel):
    name = models.CharField(max_length=200, unique=True)
    status = models.IntegerField(choices=BaseStatus.choices, default=BaseStatus.ACTIVE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "         Attributes"
        ordering = ['-id']

    def update(self, name: str):
        self.name = name
        self.save(update_fields=('name', 'updated_at'))


class AttributeValue(TimestampedModel):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=250)
    status = models.IntegerField(choices=BaseStatus.choices, default=BaseStatus.ACTIVE)

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"

    class Meta:
        verbose_name_plural = "AttributeValues"
        ordering = ['-id']

    def update(self, value: str, attribute_id: int = None):
        new_val = value.lower().capitalize()
        if attribute_id:
            self.attribute_id = attribute_id
        self.value = new_val
        self.save(update_fields=('value', 'updated_at'))

    def to_dict(self):
        return {"id": self.id, "name": self.value}
        # return {
        #     "id": self.attribute_id,
        #     "name": self.attribute.name,
        #     "attribute": {
        #         "id": self.id,
        #         "name": self.value
        #     }
        # }

    def serializer(self):
        return {
            "name": self.attribute_id,
            "value": self.id
        }


class Brand(TimestampedModel):
    name = models.CharField(max_length=200, unique=True)
    status = models.IntegerField(choices=BaseStatus.choices, default=BaseStatus.ACTIVE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "   Brands"
        ordering = ['-id']


class Measurement(TimestampedModel):
    name = models.CharField(max_length=200, unique=True)
    status = models.IntegerField(choices=BaseStatus.choices, default=BaseStatus.ACTIVE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "  Measurements"
        ordering = ['-id']


class BaseProduct(TimestampedModel):
    """ One To Many > to Outlet """
    title = models.CharField(max_length=120)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    unit = models.ForeignKey(Measurement, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(blank=True)
    upc = models.CharField(max_length=120, blank=True)  # barcode InternationalArticleNumber UPC (UniversalProductCode)
    status = models.IntegerField(choices=BaseProductStatus.choices, default=BaseProductStatus.ACTIVE)
    photos = models.JSONField(null=True, blank=True)

    objects = ProductManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "       BaseProducts"
        ordering = ['-id']

    @property
    def images(self):
        # TODO need to check status
        return self.photos

    def add_variations(self, outlet_id: int, barcode: str, color, memory, quantity, prices: dict):
        """ Create new `ProductVariation` if not exists... then save new attributes """
        new_product = self.variation.create(
            outlet_id=outlet_id,
            product_id=self.id,
            prod_code=barcode,
            original_price=prices.get("original", float(0.0)),
            selling_price=prices.get("selling", float(0.0)),
            minimal_price=prices.get("minimal", float(0.0)),
            quantity=quantity
        )
        if color:
            new_product.set_color(val=color)
        if memory:
            new_product.set_memory(val=memory)
        return new_product


class OutletProduct(TimestampedModel):
    """ all product in this outlet (ProductVariation) """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="outlet_product_user")
    # UZS = 'UZS'
    # USD = 'USD'
    # CHOICES = ((UZS, "UZS"), (USD, "USD"),)  # ((YES, "Xa"), (NO, "Yo'q"),)
    title = models.CharField(max_length=120, default="")
    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE, related_name="marketplace_product")
    product = models.ForeignKey(BaseProduct, on_delete=models.CASCADE, related_name="variation")
    px_code = models.CharField(max_length=50, blank=True)  # P-12345
    prod_code = models.CharField(max_length=50, blank=True)  # IMEI or product attribute code (variation)
    attributes = models.ManyToManyField(AttributeValue, blank=True, related_name='attributes')
    original_price = models.FloatField(default=0.0)
    selling_price = models.FloatField(default=0.0)
    minimal_price = models.FloatField(default=0.0)
    sale = models.SmallIntegerField(default=0)
    tax_percent = models.FloatField(default=0.0)  # QQS (НДС) %
    tax_amount = models.FloatField(default=0.0)  # QQS (НДС) 3 000 sum
    quantity = models.IntegerField(default=0)
    status = models.IntegerField(choices=BaseStatus.choices, default=BaseStatus.ACTIVE)

    # objects = ProductManager()

    def save(self, *args, **kwargs):

        if not self.id:
            if self.quantity > 0:
                self.status = BaseStatus.ACTIVE
            else:
                self.status = BaseStatus.INACTIVE

        else:
            if self.quantity > 0:
                self.status = BaseStatus.ACTIVE
            else:
                self.status = BaseStatus.INACTIVE

        return super(OutletProduct, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}: {self.product.title}"

    class Meta:
        verbose_name_plural = "      OutletProducts"
        ordering = ['-id']

    def add_variation_images(self, images: list):
        for image_id in images:
            if not self.variation_image.filter(instance_id=self.id, image_id=image_id).exists():
                self.variation_image.create(instance_id=self.id, image_id=image_id)

    def update_variation_image(self, images: list):
        for image_id in images:
            qs = self.variation_image.filter(instance_id=self.id, image_id=image_id)
            if qs.exists():
                qs.delete()
            self.variation_image.create(instance_id=self.id, image_id=image_id)

    def add_attributes(self, attr):
        qs = self.attributes.filter(id=attr['value'])
        if not qs.exists():
            self.attributes.add(attr['value'])

    def set_color(self, val: str):
        attr, _ = Attribute.objects.get_or_create(name="Color")
        value, _ = AttributeValue.objects.get_or_create(attribute_id=attr.id, value=val.lower().capitalize())
        self.attributes.add(value.id)

    def set_memory(self, val: str):
        attr, _ = Attribute.objects.get_or_create(name="Memory")
        value, _ = AttributeValue.objects.get_or_create(attribute_id=attr.id, value=val.lower().capitalize())
        self.attributes.add(value.id)

    @property
    def color(self):
        color = "color"
        for item in self.attributes.all():
            if item.attribute.name.lower() == color:
                color = item.value
                break
        return color

    @property
    def memory(self):
        memory = "memory"
        for item in self.attributes.all():
            if item.attribute.name.lower() == memory:
                memory = item.value
                break
        return memory

    def update_attributes(self, attributes: list):
        if self.attributes.exists():
            for attr in self.attributes.all():
                self.attributes.remove(attr.id)
        for attribute in attributes:
            self.attributes.add(attribute['value'])

    @property
    def images(self):
        return self.product.photos or self.product.images

    @property
    def currency(self):
        return Currency.get_currency_uzs().name

    # @property
    # def images(self):
    #     qs = self.variation_image.filter(instance_id=self.id)
    #     data = []
    #     if qs.exists():
    #         for item in qs:
    #             data.append({"id": item.id, "image": item.image.url})
    #     return data


class InOutProduct(TimestampedModel):
    """
    InOutProduct.objects.create(
        outlet=OutletProduct.outlet,
        product=product,
        provider=BillingAccount,
        client=BillingAccount,
        quantity=1,
        pay_type=InvoiceReceiptType.CASH,
        type=InOutType.BUYING
    )
    """
    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE)
    product = models.ForeignKey(OutletProduct, on_delete=models.CASCADE, related_name="buy_sell_product")
    provider = models.ForeignKey(OutletCustomer, on_delete=models.CASCADE, null=True, blank=True, related_name="buy_provider")
    client = models.ForeignKey(OutletCustomer, on_delete=models.CASCADE, null=True, blank=True, related_name="sell_client")
    price = models.FloatField(default=0.0)
    quantity = models.IntegerField(default=1)
    comment = models.TextField(blank=True)
    pay_type = models.IntegerField(choices=InvoiceReceiptType.choices, default=InvoiceReceiptType.CASH)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, blank=True, null=True)
    type = models.IntegerField(choices=InOutType.choices, default=InOutType.BUYING)

    class Meta:
        verbose_name_plural = "     InOutProduct"
        ordering = ['-id']

    def __str__(self):
        return f"{self.product.title} / {self.quantity}"

    @property
    def pay_type_display(self):
        return self.get_pay_type_display()

    @property
    def type_display(self):
        return self.get_type_display()

    def px_code(self):
        return self.product.px_code

    def save(self, *args, **kwargs):

        if not self.id:
            if self.type == InOutType.SELLING:
                self.price = self.product.selling_price
            else:
                self.price = self.product.original_price

        return super(InOutProduct, self).save(*args, **kwargs)


class SalesProduct(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sales")
    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE, null=True, blank=True)
    client = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="anonymous_client")
    product = models.ForeignKey(OutletProduct, on_delete=models.CASCADE, related_name="sales_product")
    quantity = models.IntegerField(default=1)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "    SalesProducts"
        ordering = ['-id']

    def __str__(self):
        return f"{self.product.title} / {self.quantity}"


class InternationProduct(TimestampedModel):
    barcode_number = models.CharField(max_length=256, blank=True)
    barcode_formats = models.CharField(max_length=256, blank=True)
    mpn = models.CharField(max_length=256, blank=True)
    model = models.CharField(max_length=256, blank=True)
    asin = models.CharField(max_length=256, blank=True)
    title = models.CharField(max_length=256, blank=True)
    category = models.CharField(max_length=256, blank=True)
    last_child = models.CharField(max_length=256, blank=True)
    manufacturer = models.CharField(max_length=256, blank=True)
    brand = models.CharField(max_length=256, blank=True)
    ingredients = models.CharField(max_length=256, blank=True)
    nutrition_facts = models.CharField(max_length=256, blank=True)
    color = models.CharField(max_length=120, blank=True)
    gender = models.CharField(max_length=256, blank=True)
    material = models.CharField(max_length=256, blank=True)
    pattern = models.CharField(max_length=256, blank=True)
    size = models.CharField(max_length=256, blank=True)
    length = models.CharField(max_length=120, blank=True)
    width = models.CharField(max_length=120, blank=True)
    height = models.CharField(max_length=120, blank=True)
    weight = models.CharField(max_length=120, blank=True)
    release_date = models.CharField(max_length=256, blank=True)
    description = models.TextField(blank=True)
    images = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.barcode_number

    class Meta:
        verbose_name_plural = "InternationProducts"
        ordering = ['-id']

    def to_dict(self):
        return {
            "title": self.title,
            "category": self.last_child,
            "brand": self.brand,
            "upc": self.barcode_number,
            "color": self.color,
            "memory": self.size,
            "images": self.images
        }
