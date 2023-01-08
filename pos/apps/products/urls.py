from django.urls import path
from . import views

app_name = "products"
# api/v1/products/<path to view>/

urlpatterns = [
    path("attribute/add/", views.AttributeAddView.as_view(), name="add_attribute"),
    path("attribute/", views.AttributeViewSet.as_view(), name="attribute"),
    path("attribute/<int:pk>/", views.AttributeViewSet.as_view(), name="attribute_pk"),
    path("attribute/list/", views.AttributeViewList.as_view(), name="attribute_list"),

    path("product/list/", views.ProductListView.as_view(), name="product_list"),

    path("product/", views.ProductViewSet.as_view(), name="product"),
    path("product/<int:pk>/", views.ProductViewSet.as_view(), name="product_pk"),
    path("variation/update/<int:pk>/", views.OutletProductViewSet.as_view(), name="variation_update"),

    path("product/income/", views.IncomeProductView.as_view(), name="income_product"),

    path("unit/", views.UnitViewSet.as_view(), name="unit"),
    path("unit/<int:pk>/", views.UnitViewSet.as_view(), name="unit_pk"),

    path("brand/", views.BrandViewSet.as_view(), name="brand"),
    path("brand/<int:pk>/", views.BrandViewSet.as_view(), name="brand_pk"),
]
