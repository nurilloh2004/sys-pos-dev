from django.urls import path
from . import views

app_name = "outlets"
# api/v1/outlets/

urlpatterns = [
    path("outlet/", views.OutletViewSet.as_view(), name="outlet"),
    path("outlet/<int:pk>/", views.OutletViewSet.as_view(), name="outlet_pk"),

    path("my-outlet/", views.MyOutletView.as_view(), name="my_outlet"),
    path("outlet-branches/<int:pk>/", views.OutletBranchesView.as_view(), name="outlet_branches"),

    path("outlet-members/", views.OutletMemberListView.as_view(), name="outlet_members"),
    path("member/detail/<int:pk>/", views.OutletMemberDetailView.as_view(), name="member_detail"),

    path("outlet-customers/", views.OutletCustomerListView.as_view(), name="outlet_customers"),  # Должник / Поставщик
    path("customer-detail/<int:pk>/", views.OutletCustomerDetailView.as_view(), name="customer_detail"),
    path("customer-history/<int:pk>/", views.OutletCustomerHistoryView.as_view(), name="outlet_history"),  # detail

    path("product/list/", views.OutletProductList.as_view(), name="outlet_product_list"),
    path("product/detail/<int:pk>/", views.OutletProductDetail.as_view(), name="outlet_product_detail"),

    path("product/scanner/", views.ProductScannerView.as_view(), name="product_scanner"),  # IMEI scan
    path("product/search/", views.SearchProductView.as_view(), name="global_search"),
    path("product/single/search/", views.SingleProductSearchView.as_view(), name="single_search"),  # find item in shop

    # CashBox APIs
    path("cashbox/", views.OutletCashBoxDetailView.as_view(), name="outlet_cashbox"),
    path("invoice/checkout/", views.CashBoxCheckoutView.as_view(), name="invoice_checkout"),
    path("checkout/confirm/", views.CashBoxCheckoutConfirmView.as_view(), name="checkout_confirm"),
]
