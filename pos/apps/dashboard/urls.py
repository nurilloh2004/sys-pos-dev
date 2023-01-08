from django.urls import path
from . import views

app_name = "dashboard"
# api/v1/dashboard/

urlpatterns = [
    path("permissions/list/", views.SelectedPermissionList.as_view(), name='permissions'),

    path("currency/", views.CurrencyViewSet.as_view(), name="brand"),
    path("currency/<int:pk>/", views.CurrencyViewSet.as_view(), name="brand_pk"),

    path("category/list/", views.CategoryListView.as_view(), name="category_list"),
    path("category/", views.CategoryViewSet.as_view(), name="category_create"),
    path("category/<int:pk>/", views.CategoryViewSet.as_view(), name="category_pk"),

    path("info/", views.DashboardViewSet.as_view(), name='base_info'),
]
