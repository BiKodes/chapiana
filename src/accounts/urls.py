from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"users", UserCreateViewSet, basename="create_user")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("acounts/", include(router.urls))
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)