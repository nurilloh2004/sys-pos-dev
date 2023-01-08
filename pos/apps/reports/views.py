from rest_framework.permissions import IsAuthenticated
from apps.core.services.generics import CustomAPIView, CustomListView
from . models import Invoice, Outlet, InvoiceReceipt
from apps.core.services.status import *
from apps.core.services.generics import POSResponse
from . import serializers as ser


class InvoiceDetailView(CustomAPIView):
    """
    GET: {{BASE}}api/v1/reports/invoice/detail/{id}/
    """
    serializer_class = ser.InvoiceDetailSerializer
    permission_classes = [IsAuthenticated]
    queryset = Invoice.objects.all()
    tags = ["Invoice detail API"]

    def get(self, request, pk):
        try:
            invoice = Invoice.objects.get(id=pk)
            serializer = self.serializer_class(instance=invoice)
            return self.success_response(results=serializer.data)
        except Exception as e:
            self.code = POSResponse.CODE_3
            self.error_message = POSResponse.MSG_3
            self.exception = e.args
            return self.error_response()


class OutletInvoiceListView(CustomListView):
    serializer_class = ser.InvoiceListSerializer
    permission_classes = [IsAuthenticated]
    tags = ["Invoice list API"]
    param = "?"

    def get_queryset(self):
        user = self.request.user
        params = self.request.query_params
        outlet = self.get_user_main_shop()

        invoice_id = params.get('invoice_id', None)
        status = params.get('status', None)
        outlet_id = params.get('outlet_id', None)
        pay_type = params.get('pay_type', None)
        order_by = params.get('order', None)

        queryset = Invoice.objects.filter(outlet_id=outlet.id)

        if invoice_id:
            queryset = queryset.filter(invoice_id__icontains=invoice_id)

        if status:
            queryset = queryset.filter(status=status)

        if outlet_id:
            queryset = queryset.filter(outlet_id=outlet_id)

        if pay_type:
            queryset = queryset.filter(
                id__in=[receipt.invoice.id for receipt in InvoiceReceipt.objects.filter(invoice_id__in=queryset, pay_type=pay_type)]
            )

        if order_by:
            queryset = queryset.order_by(self.order_by_lookup(by=order_by))

        return queryset


class OutletHistoryListView(CustomListView):
    """
    GET: {{BASE}}api/v1/reports/outlets/history/list/
    """
    serializer_class = ser.InvoiceListSerializer
    permission_classes = [IsAuthenticated]
    tags = ["Report history List API"]
    param = "?"

    def get_queryset(self):
        user = self.request.user
        params = self.request.query_params

        query = params.get('query', None)
        order_by = params.get('order', None)

        outlets = Outlet.objects.filter(owner_id=user.id)

        if outlets:
            invoices = Invoice.objects.filter(outlet_id__in=[outlet.id for outlet in outlets.all()])
            if order_by:
                invoices = invoices.order_by(self.order_by_lookup(by=order_by))
            return invoices
        else:
            return []


class OutletHistoryDetailView(CustomAPIView):
    """
    GET: {{BASE}}api/v1/reports/outlets/history/detail/{id}/
    """
    serializer_class = ser.InvoiceDetailSerializer
    permission_classes = [IsAuthenticated]
    queryset = Invoice.objects.all()
    tags = ["Report detail API"]

    def get(self, request, pk):
        try:
            invoice = Invoice.objects.get(id=pk)
            serializer = self.serializer_class(instance=invoice)
            return self.success_response(results=serializer.data)
        except Exception as e:
            self.code = POSResponse.CODE_3
            self.error_message = POSResponse.MSG_3
            self.exception = e.args
            return self.error_response()
