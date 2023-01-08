from email.policy import default
from apps.core.services.response import ResponseController
from apps.core.services.status import *
from apps.core.services.generics import CustomListView, CustomCreateUpdateView, CustomAPIView, CustomModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.dashboard.models import SelectedPermission
from apps.accounts.models import User
from . import serializers as ser
from apps.core.services.generics import POSResponse
from . models import Currency, Category
from apps.accounts.serializers import UserDetailSerializer
from apps.products.models import SalesProduct, OutletProduct
from apps.reports.models import Invoice, InvoiceProduct

class SelectedPermissionList(CustomListView):
    """ GET: {{BASE}}api/v1/dashboard/permissions/list/ """
    serializer_class = ser.SelectedPermissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SelectedPermission.objects.all()


class DashboardViewSet(CustomAPIView):
    """ GET BASE Dashboard information """
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]
    model = User

    def get(self, request, *args, **kwargs):
        outlet = self.get_user_main_shop()
        queryset = OutletProduct.objects.filter(outlet_id=outlet.id)
        context = {
            'total_products': queryset.filter(Q(user=request.user) | Q(outlet__user = request.user) | Q(outlet__owner =request.user)).count(),
            'products_saled_in_oneweek': SalesProduct.objects.filter(Q(outlet_id=outlet.id), Q(user=request.user) | Q(outlet__user = request.user) | Q(outlet__owner =request.user)).filter(created_at__gte=timezone.now() - timedelta(days=7)).count(),
            'products_price_saled_in_oneweek': SalesProduct.objects.filter(Q(outlet_id=outlet.id), created_at__gte=timezone.now() - timedelta(days=7)).aggregate(total_sum = Sum('product__original_price'))['total_sum'],
            'users': User.objects.filter(outlet_product_user__outlet_id=outlet.id).count(),
            'checks': Invoice.objects.filter(Q(status=InvoiceStatus.PAID), Q(created_at__gte = timezone.now() - timedelta(days=7))).count(),
            'declined_checks': queryset.filter(status=BaseStatus.DELETED).count(),
            'count_of_user_many_saled': Invoice.objects.filter(Q(outlet_id=outlet.id), Q(status=InvoiceStatus.PAID)).values('seller').annotate(total_sum = Sum('total')).order_by('-total_sum')[:10],
            'products_most_of_saled': queryset.filter(Q(user=request.user) | Q(outlet__user = request.user) | Q(outlet__owner =request.user)).values('product')

        }
        return self.success_response(results=context)






class CurrencyViewSet(CustomModelViewSet):
    """ ViewSet {{BASE}}api/v1/dashboard/currency/ """
    tags = ["Currency API"]
    serializer_class = ser.CurrencySerializer
    queryset = Currency.objects.filter(status=BaseStatus.ACTIVE)
    model = Currency


class CategoryListView(CustomListView):
    """ GET {{BASE}}api/v1/dashboard/category/list/ """
    serializer_class = ser.CategorySerializer
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.filter(status=BaseStatus.ACTIVE)
    tags = ["Category list"]


class CategoryViewSet(CustomCreateUpdateView):
    serializer_class = ser.CategorySerializer
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.filter(status=BaseStatus.ACTIVE)
    model = Category
    tags = ["Category API"]

    def create(self, request, *args, **kwargs):
        data = request.data
        parent = None
        qs = Category.objects.filter(name__iexact=data["name"])
        if qs.exists():
            self.update_error_text(catch=data["name"])
            self.code = POSResponse.CODE_1
            self.error_message = POSResponse.MSG_1
            return self.error_response()
        try:
            if data["parent"]:
                parent = Category.objects.get(id=data["parent"])
                data["parent"] = parent.id

            category = Category.objects.create(parent=parent, name=data["name"])
            serializer = self.serializer_class(instance=category)
            return self.success_response(results=serializer.data)
        except Exception as e:
            self.code = POSResponse.CODE_3
            self.error_message = POSResponse.MSG_3
            self.exception = e.args
            return self.error_response()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        data = request.data
        return self.custom_update(data=data, partial=partial)



