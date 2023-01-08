from django.urls import path
from . import views

app_name = "address"
# api/v1/outlets/

urlpatterns = [
    path("regions/", views.RegionsAPIView.as_view(), name="regions"),
    path("district/<int:pk>/", views.DistrictAPIView.as_view(), name="districts"),
]
