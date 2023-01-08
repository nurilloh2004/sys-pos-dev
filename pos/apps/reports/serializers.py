from rest_framework import serializers
from apps.accounts.serializers import UserMiniSerializer
from apps.outlets.serializers import OutletShortSerializer, OutletProductsShortSerializer
from apps.dashboard.serializers import CurrencySerializer
from .models import Invoice, InvoiceProduct, InvoiceReceipt


class InvoiceReceiptDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvoiceReceipt
        fields = (
            "id",
            "invoice",
            "receipt_no",
            "pay_type",
            "amount_cash",
            "amount_card",
            "status"
        )


class InvoiceReceiptShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvoiceReceipt
        fields = (
            "id",
            "invoice",
            "receipt_no",
            "pay_type",
            "amount_cash",
            "amount_card",
            "status"
        )


class InvoiceReceiptMiniSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvoiceReceipt
        fields = ("id", "pay_type", "receipt_no", "amount_cash", "amount_card", "total")


class InvoiceDetailSerializer(serializers.ModelSerializer):
    """ Full single invoice serializers """
    outlet = OutletShortSerializer()
    seller = UserMiniSerializer(source='seller.user')
    currency = CurrencySerializer()

    class Meta:
        model = Invoice
        fields = (
            "id",
            "outlet",
            "invoice_id",
            "seller",
            "total",
            "comment",
            "currency",
            "expire_in",
            "created_at",
        )

    def to_representation(self, instance: Invoice):
        data = super(InvoiceDetailSerializer, self).to_representation(instance=instance)

        products = []
        qs = InvoiceReceipt.objects.filter(invoice_id=instance.id)
        receipts = None
        if instance.products.exists():
            for product in instance.products.all():
                serializer = OutletProductsShortSerializer(instance=product)
                item = InvoiceProduct.objects.get(product_id=product.id, invoice_id=instance.id)
                products.append({**serializer.data, "quantity": item.count, "total": item.total})
        data['products'] = products
        data['products_qty'] = len(products)

        if qs.exists():
            receipts = InvoiceReceiptMiniSerializer(instance=qs.last()).data

        data['receipts'] = receipts
        return data


class InvoiceListSerializer(serializers.ModelSerializer):
    outlet = OutletShortSerializer()
    seller = UserMiniSerializer(source='seller.user')

    class Meta:
        model = Invoice
        fields = (
            "id",
            "outlet",
            "invoice_id",
            "seller",
            "total",
            "created_at",
        )

    # def to_representation(self, instance: Invoice):
    #     data = super(InvoiceListSerializer, self).to_representation(instance=instance)
    #
    #     products = []
    #     qs = InvoiceReceipt.objects.filter(invoice_id=instance.id)
    #     receipts = None
    #     if instance.products.exists():
    #         for product in instance.products.all():
    #             serializer = InvoiceProductsShortSerializer(instance=product)
    #             item = InvoiceProduct.objects.get(product_id=product.id, invoice_id=instance.id)
    #             products.append({**serializer.data, "quantity": item.count, "total": item.total})
    #     data['products'] = products
    #
    #     if qs.exists():
    #         receipts = InvoiceReceiptMiniSerializer(instance=qs.last()).data
    #
    #     data['receipts'] = receipts
    #     return data
