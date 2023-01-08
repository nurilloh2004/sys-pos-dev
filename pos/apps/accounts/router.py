from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

app_name = "accounts"
# api/v1/accounts/

urlpatterns = [
    path("role/", views.RoleViewSet.as_view(), name="role"),  # Role list for auth user
    path("role/<int:pk>/", views.RoleViewSet.as_view(), name="role_pk"),
    path("owner/roles/", views.OwnerRolesList.as_view(), name='owner_roles'),  # Owner all roles

    path("create-owner/", views.CreateOwnerAPIView.as_view(), name="create_owner"),
    path("create-member/", views.CreateMemberAPIView.as_view(), name="create_member"),
    path("delete-member/<int:pk>/", views.MemberDeleteViewView.as_view(), name="member_delete"),  # Delete

    path("create-customer/", views.CreateCustomerUserAPIView.as_view(), name="create_customer"),  # Должник / Поставщик
]
