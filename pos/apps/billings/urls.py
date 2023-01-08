from django.urls import path
from . import views

app_name = "billings"
# api/v1/billings/

urlpatterns = [
    path("profile/", views.ProfileViewSet.as_view(), name='profile'),
    path("profile/<int:pk>/", views.ProfileViewSet.as_view(), name='profile_pk'),
]
