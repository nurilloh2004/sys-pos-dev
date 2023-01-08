from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Currency, Outlet, OutletMember, OutletCustomer
from apps.core.services.generics import CustomGenericAPIView, CustomListView, CustomCreateUpdateView, CustomAPIView
from apps.products.models import BaseProduct, OutletProduct, InOutProduct
from apps.accounts.serializers import UserListSerializer
from apps.core.services.status import *
from apps.core.services.generics import POSResponse
from apps.core.services.permissions import HasCreateOutletPermission
from . import serializers as ser
from apps.products.serializers import BaseProductSerializer
from .utils.services import OutletController, CheckoutController
from apps.products.utils.services import ProductController
from apps.reports.serializers import InvoiceDetailSerializer
from apps.reports.models import Invoice, InvoiceProduct, InvoiceReceipt


class OutletViewSet(CustomCreateUpdateView, OutletController):
    queryset = Outlet.objects.all()
    serializer_class = ser.CreateOutletSerializer
    permission_classes = [IsAuthenticated, HasCreateOutletPermission]
    model = Outlet
    tags = ["Outlets API"]

    def get(self, request, *args, **kwargs):
        try:
            serializer = ser.OutletDetailSerializer(instance=Outlet.objects.get(pk=self.kwargs["pk"]))
            return self.success_response(results=serializer.data)
        except Exception as e:
            self.code = POSResponse.CODE_3
            self.error_message = POSResponse.MSG_3
            self.exception = e.args
            return self.error_response()

    def update(self, request, *args, **kwargs):
        """
            "address_name": "Sugalli ota 5",
            "latitude": 41.111111,
            "longitude": 71.111111,
            "region": 1,
            "district": 1,
            "images": [1],
        """
        data = request.data

        partial = kwargs.pop('partial', False)
        instance = self.get_instance()
        self.get_region()
        self.get_district()

        is_images = False
        if "images" in data and data["images"]:
            self.validator_images()
            is_images = True

        data.pop("parent")
        data["user"] = instance.user.id
        if "working_hours" in data and data["working_hours"]:
            self.create_working_day(shop=instance, working_hours=data["working_hours"])

        serializer = self.serializer_class(instance=instance, data=data, partial=partial)

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        instance.update_address(**data)
        if is_images:
            instance.add_outlet_image(images=data["images"])
        return self.success_response(results=serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data
        user_id = request.user.id
        data["owner"] = user_id
        data["user"] = user_id
        main = Outlet.objects.filter(user_id=user_id, parent__isnull=True, type=OutletType.MAIN)
        if main.exists() and not data["parent"]:
            return self.outlet_data(instance=main.last())

        region_id = self.get_region()
        district_id = self.get_district()

        parent = None
        if "parent" in data and data["parent"]:
            parent = self.get_shop_by_id(branch_id=data["parent"]).id

        is_images = False
        if "images" in data and data["images"]:
            self.validator_images()
            is_images = True

        data["parent"] = parent
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        outlet = serializer.instance

        self.create_shop_address(shop=outlet, region_id=region_id, district_id=district_id)

        if is_images:
            outlet.add_outlet_image(images=data["images"])
        self.shop_working_day(shop=outlet)

        return self.outlet_data(instance=outlet)

    def outlet_data(self, instance: Outlet):
        serializer = ser.OutletDetailSerializer(instance=instance)
        return self.success_response(results=serializer.data)


class MyOutletView(CustomAPIView, OutletController):
    queryset = Outlet.objects.all()
    serializer_class = ser.OutletDetailSerializer
    permission_classes = [IsAuthenticated]
    tags = ["Get (Main outlet)"]

    def get(self, request):
        serializer = self.serializer_class(instance=self.get_user_main_shop())
        return self.success_response(results=serializer.data)


class OutletBranchesView(CustomListView):
    """
    GET: {{BASE}}api/v1/outlets/outlet-branches/{id}/
    """
    serializer_class = ser.OutletDetailSerializer
    permission_classes = [IsAuthenticated]
    tags = ["Get (Outlet branches)"]

    def get_queryset(self):
        return Outlet.objects.filter(parent_id=self.kwargs.get('pk', 0))


class OutletMemberListView(CustomListView):
    serializer_class = ser.OutletMemberListSerializer
    permission_classes = [IsAuthenticated]
    tags = ["Outlet members list API"]
    param = "?"

    def get_queryset(self):
        user = self.request.user
        params = self.request.query_params
        outlet = self.get_user_main_shop()

        query = params.get('query', None)
        member_type = params.get('type', 1)
        order_by = params.get('order', None)

        # queryset = OutletMember.objects.filter(
        #     Q(outlet__parent_id=outlet.id) | Q(outlet_id=outlet.id),
        #     status=BaseStatus.ACTIVE, type=member_type
        # )
        queryset = OutletMember.objects.filter(outlet_id=outlet.id, status=BaseStatus.ACTIVE, type=member_type)

        if query is not None:
            self.param = query
            queryset = queryset.filter(
                Q(user__username__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(user__fullname__icontains=query) |
                Q(user__phone__icontains=query)
            )

        if member_type:
            queryset = queryset.filter(type=member_type)

        if order_by:
            queryset = queryset.order_by(self.order_by_lookup(by=order_by))

        return queryset


class OutletMemberDetailView(CustomAPIView):
    serializer_class = ser.OutletMemberDetailSerializer
    permission_classes = [IsAuthenticated]
    tags = ["Outlet member detail API <member_id>"]

    def get(self, request, pk):
        try:
            member = OutletMember.objects.get(id=pk)
            serializer = self.serializer_class(instance=member)
            return self.success_response(results=serializer.data)
        except Exception as e:
            self.update_error_text(catch=pk)
            self.code = POSResponse.CODE_4
            self.error_message = POSResponse.MSG_4
            self.exception = e.args
            return self.error_response()


class OutletCustomerListView(CustomListView):
    """
    GET: {{BASE}}api/v1/outlets/outlet-customer/
    QUERY params:
    ?query=something
    &type=2&
    order=ASC

    Должник / Поставщик
    """

    serializer_class = ser.OutletCustomerListSerializer
    permission_classes = [IsAuthenticated]
    tags = ["Outlet provider/customer list API"]
    param = "?"

    def get_queryset(self):
        user = self.request.user
        params = self.request.query_params
        outlet = self.get_user_main_shop()

        query = params.get('query', None)
        customer_type = params.get("type", 2) if params.get("type", 2) else 2
        order_by = params.get('order', None)

        queryset = OutletCustomer.objects.filter(
            Q(outlet__parent_id=outlet.id) | Q(outlet_id=outlet.id), type=customer_type
        )

        if query is not None:
            self.param = query
            queryset = queryset.filter(
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(user__fullname__icontains=query) |
                Q(user__phone__icontains=query)
            )
        if order_by:
            queryset = queryset.order_by(self.order_by_lookup(by=order_by))

        return queryset


class OutletCustomerDetailView(CustomAPIView):
    """
    GET: {{BASE}}api/v1/outlets/customer-detail/{id}/
    Клиент / Поставщик
    """
    serializer_class = ser.OutletCustomerDetailSerializer
    permission_classes = [IsAuthenticated]
    tags = ["Outlet customer detail API <customer_id>"]

    def get(self, request, pk):
        qs = OutletCustomer.objects.filter(id=pk)
        if qs.exists():
            serializer = self.serializer_class(instance=qs.last())
            return self.success_response(results=serializer.data)
        else:
            self.update_error_text(catch=pk)
            self.code = POSResponse.CODE_4
            self.error_message = POSResponse.MSG_4
            return self.error_response()


class OutletCustomerHistoryView(CustomListView):
    """
    GET: {{BASE}}api/v1/outlets/customer-history/{id}/
    Клиент / Поставщик
    """
    serializer_class = ser.OutletCustomerHistorySerializer
    permission_classes = [IsAuthenticated]
    tags = ["Outlet customer history list <customer_id>"]
    param = "?"

    def get_queryset(self):
        user = self.request.user
        try:
            customer = OutletCustomer.objects.get(id=self.kwargs['pk'])
            params = self.request.query_params
            outlet = self.get_user_main_shop()

            query = params.get('query', None)
            order_by = params.get('order', None)

            if customer.type == OutletCustomerType.CLIENT:
                queryset = InOutProduct.objects.filter(outlet_id=outlet.id, client_id=customer.id)
            else:
                queryset = InOutProduct.objects.filter(outlet_id=outlet.id, provider_id=customer.id)

            if order_by:
                queryset = queryset.order_by(self.order_by_lookup(by=order_by))

            return queryset
        except Exception as e:
            self.update_error_text(catch="Invalid customer")
            self.code = POSResponse.CODE_4
            self.error_message = POSResponse.MSG_4
            self.exception = e.args
            return self.error_response()


class OutletProductList(CustomListView, OutletController):
    """
    {{BASE}}api/v1/outlets/product/list/
    optional params: ?branch_id=12

    order by ASC (1, 2, 3) default
    order by DESC (3, 2, 1)
    """
    serializer_class = ser.ProductListSerializer
    permission_classes = [IsAuthenticated]
    tags = ["Outlet product list"]

    def get_queryset(self):
        params = self.request.query_params
        branch_id = params.get('branch_id', None)

        category_ids = self.parse_url_ids(ids=params.get('category_ids', None))
        brand_ids = self.parse_url_ids(ids=params.get('brand_ids', None))
        attributes_ids = self.parse_url_ids(ids=params.get('attributes_ids', None))

        status = params.get('status', None)
        order_by = params.get('order', None)

        if branch_id:
            outlet = self.get_shop_by_id(branch_id=branch_id)
        else:
            outlet = self.get_user_main_shop()

        queryset = OutletProduct.objects.filter(outlet_id=outlet.id)

        if status:
            queryset = queryset.filter(status=status)

        if category_ids:
            queryset = queryset.filter(product__category_id__in=category_ids)

        if brand_ids:
            queryset = queryset.filter(product__brand_id__in=brand_ids)

        if attributes_ids:
            queryset = queryset.filter(attributes__in=attributes_ids)

        if order_by:
            return queryset.order_by(self.order_by_lookup(by=order_by))

        return queryset


class ProductScannerView(CustomGenericAPIView, ProductController):
    """
    POST: {{BASE}}api/v1/outlets/product/scanner/
    {
        "code": "887276218830"
    }
    """
    serializer_class = ser.ProductScannerSerializer
    permission_classes = [IsAuthenticated]
    tags = ["Product Scanner API"]

    def post(self, request, *args, **kwargs):
        try:
            data = self.get_upc_detail(upc_code=request.data["code"])
            return self.success_response(results=data)
        except Exception as e:
            self.code = POSResponse.CODE_3
            self.error_message = POSResponse.MSG_3
            self.exception = e.args
            return self.error_response()


class SearchProductView(CustomGenericAPIView, OutletController):
    """
     GET: api/v1/outlets/product/search/?query=samsung
     ?query=samsung

     order by ASC (1, 2, 3) default
     order by DESC (3, 2, 1)
    """
    serializer_class = ser.ProductSearchSerializer
    permission_classes = [IsAuthenticated]
    tags = ["Global Product search API"]
    param = "?"

    def get(self, request, *args, **kwargs):

        queryset = self.get_queryset()
        if queryset:
            serializer = self.serializer_class(queryset, many=True)
            return self.success_response(results=serializer.data)
        else:
            self.update_error_text(catch=self.param)
            self.code = POSResponse.CODE_4
            self.error_message = POSResponse.MSG_4
            return self.error_response()

    def get_queryset(self):
        params = self.request.query_params
        query = params.get('query', None)
        status = params.get('status', None)
        order_by = params.get('order', None)

        outlet = self.get_user_main_shop()

        queryset = OutletProduct.objects.filter(outlet_id=outlet.id)

        if query is not None:
            """
            product__title > BaseProduct
            title > ProductVariation
            px_code
            prod_code
            """
            self.param = query
            queryset = queryset.filter(
                Q(product__title__icontains=query) |
                Q(title__icontains=query) |
                Q(px_code__icontains=query) |
                Q(prod_code__icontains=query)
            )

        if status:
            queryset = queryset.filter(status=status)

        if order_by:
            return queryset.order_by(self.order_by_lookup(by=order_by))

        return queryset


class SingleProductSearchView(CustomGenericAPIView, OutletController):
    """
     GET: api/v1/outlets/product/single/search/?query=IMEI
    """
    serializer_class = ser.SingleSearchSerializer
    permission_classes = [IsAuthenticated]
    tags = ["Single Product search API (IMEI)"]
    param = "?"

    def get(self, request, *args, **kwargs):
        query = self.request.query_params.get('query', None)
        outlet = self.get_user_main_shop()

        if query is not None:
            qs = OutletProduct.objects.filter(
                Q(title__icontains=query) | Q(px_code__icontains=query) | Q(prod_code__icontains=query), outlet_id=outlet.id
            )
            if qs.exists():
                serializer = self.serializer_class(instance=qs[0])
                return self.success_response(results=serializer.data)
            else:
                self.param = query
                self.update_error_text(catch=self.param)
                self.code = POSResponse.CODE_4
                self.error_message = POSResponse.MSG_4
                return self.error_response()
        else:
            self.param = query
            self.update_error_text(catch=self.param)
            self.code = POSResponse.CODE_4
            self.error_message = POSResponse.MSG_4
            return self.error_response()


class OutletProductDetail(CustomAPIView):
    queryset = BaseProduct.objects.all()
    serializer_class = BaseProductSerializer
    permission_classes = [IsAuthenticated]
    tags = ["Outlet product full detail"]

    def get(self, request, pk):
        qs = BaseProduct.objects.filter(id=pk)
        if qs.exists():
            serializer = self.serializer_class(instance=qs.last())
            return self.success_response(results=serializer.data)

        else:
            self.update_error_text(catch=pk)
            self.code = POSResponse.CODE_4
            self.error_message = POSResponse.MSG_4
            return self.error_response()


class OutletCashBoxDetailView(CustomAPIView):
    """
    GET: {{BASE}}api/v1/outlets/cashbox/
    """
    serializer_class = ser.OutletCashBoxSerializer
    permission_classes = [IsAuthenticated]
    tags = ["Outlet Cashbox API"]

    def get(self, request):
        outlet = self.get_user_main_shop()
        serializer = self.serializer_class(instance=outlet.get_shop_cash())
        return self.success_response(requests=serializer.data)


class CashBoxCheckoutView(CustomAPIView, CheckoutController):
    """
    {{BASE}}api/v1/outlets/checkout/
    type > CASH = 1
    type > CARD = 2
    type > CASH_CARD = 4
    type > CREDIT = 8
    {
        "type": 1,
        "product_ids": [5, 6, 7],
        "client": null,
        "cash": 500,
        "card": 200
    }
    """
    serializer_class = InvoiceDetailSerializer
    permission_classes = [IsAuthenticated]
    tags = ["Outlet product full detail"]

    def post(self, request):
        user = request.user
        data = request.data

        pay_type, cash, card = self.validate_payment_type()

        outlet = self.get_user_main_shop()
        buyer = self.get_buyer_by_id()  # Billing Account
        product_ids = []
        total = 0

        for item in data["product_ids"]:
            product = OutletProduct.objects.get(id=item)
            if product.quantity == 0:
                raise CustomValidationError(debug="Out of stock")
            product_ids.append(product.id)
            total += product.selling_price

        if (pay_type == InvoiceReceiptType.CASH_CARD) and int(total) != int(cash + card):
            self.code = POSResponse.CODE_18
            self.error_message = POSResponse.MSG_18
            return self.error_response()

        qs = Invoice.objects.filter(
            outlet_id=outlet.id,
            seller_id=user.id,
            buyer_id=buyer.id,
            products__in=product_ids,
            status=InvoiceStatus.DRAFT
        )

        if qs.exists():
            qs.delete()

        currency = Currency.get_currency_uzs()

        invoice = Invoice.objects.create(
            outlet_id=outlet.id,
            seller_id=user.id,
            buyer_id=buyer.id,
            subtotal=total,
            total=total,
            comment="Invoice created",
            currency_id=currency.id
        )

        for product_id in product_ids:
            InvoiceProduct.objects.create(product_id=product_id, invoice_id=invoice.id)

        InvoiceReceipt.objects.create(
            invoice_id=invoice.id,
            pay_type=pay_type,
            amount_cash=cash,
            amount_card=card,
            total=total
        )

        serializer = self.serializer_class(instance=invoice)
        return self.success_response(results=serializer.data)


class CashBoxCheckoutConfirmView(CustomAPIView, OutletController):
    """
    {{BASE}}api/v1/outlets/checkout/confirm/
    """
    serializer_class = InvoiceDetailSerializer
    permission_classes = [IsAuthenticated]
    tags = ["Outlet product full detail"]

    def post(self, request):
        user = request.user
        try:
            invoice = Invoice.objects.get(id=request.data["invoice_id"])
            invoice.status = InvoiceStatus.PAID
            invoice.save()

            self.update_cash_box(shop=invoice.outlet, plus=invoice.total)
            self.update_quantity_in_market(invoice=invoice)

            # for product in invoice.products.all():
            #     print("update_quantity_in_market .....", product, type(product))
            #     self.track_product(
            #         product=product,
            #         action_type=InOutType.SELLING,
            #         pay_type=data['pay_type'],
            #         provider_id=provider.id,
            #         quantity=1
            #     )
            #     OutletProduct.objects.filter(id=product.id).update(quantity=F('quantity') - 1)

            receipt = invoice.get_invoice_receipt()

            self.create_transaction(
                invoice=invoice,
                origin=invoice.buyer,
                dest=invoice.seller,
                pay_method=receipt.pay_type,
                reason=TransactionReason.SELLING,
                amount=invoice.total)

            invoice.confirm_receipt(hook=self.reporter, msg=f"{invoice.invoice_id}: Invoice payment successfully")

            if receipt.pay_type == InvoiceReceiptType.CREDIT:
                invoice.buyer.user.user_balance.update_user_balance(minus=receipt.total)

            return self.success_response()
        except Exception as e:
            self.code = POSResponse.CODE_3
            self.error_message = POSResponse.MSG_3
            self.exception = e.args
            return self.error_response()
