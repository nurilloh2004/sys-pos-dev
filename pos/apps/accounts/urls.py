from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

app_name = "auth"
# api/v1/auth/

router = DefaultRouter()
router.register("user", views.UserViewSet, basename="user")


urlpatterns = [
    path("user/me/", views.UserViewSet.as_view(), name='auth'),
    path("send-otp/", views.SendOtpAPIView.as_view(), name="send_otp"),
    path("verify-otp/", views.VerifyOtpAPIView.as_view(), name="verify_otp"),
    path("login/", views.LoginAPIView.as_view(), name="login"),
    path("reset-password/", views.ResetPasswordAPIView.as_view(), name="reset_password"),
]
