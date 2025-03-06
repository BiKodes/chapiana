from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from rest_framework.routers import DefaultRouter
from src.accounts.views import RegisterViewSet, LoginViewSet, LogoutViewSet, OneTimePassword, ForgotPasswordViewSet


router = DefaultRouter()
router.register(r"register", RegisterViewSet, basename="register-user")
router.register(r"login", LoginViewSet, basename="login-user")
router.register(r"logout", LogoutViewSet, basename="logout-user")
router.register(r"otp", OneTimePassword, basename="one-time-password")
router.register(r"password", ForgotPasswordViewSet, basename="forgot-password")

app_name = "accounts"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("acounts/", include(router.urls))
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)