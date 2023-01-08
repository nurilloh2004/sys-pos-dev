from django.urls import path
from . import views

app_name = "reports"
# api/v1/reports/<path to view>/


urlpatterns = [
    path("invoice/detail/<int:pk>/", views.InvoiceDetailView.as_view(), name="invoice_detail"),
    path("invoice/list/", views.OutletInvoiceListView.as_view(), name="invoice_list"),
    path("outlets/history/list/", views.OutletHistoryListView.as_view(), name="history_list"),
    path("outlets/history/detail/<int:pk>/", views.OutletHistoryDetailView.as_view(), name="history_detail"),
]
