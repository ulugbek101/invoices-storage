from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("app_main.urls")),
]


if settings.DEBUG:
    urlpatterns += static(prefix=settings.STATIC_URL, document_root=settings.STATIC_ROOT)
