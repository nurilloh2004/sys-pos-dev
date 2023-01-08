"""
Posox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="POSOX API",
        default_version="v1",
        description="For any questions, contact https://t.me/Fatabaeva",
        contact=openapi.Contact(email="dts@gmail.com")
    ),
    public=True,
    permission_classes=(),
    authentication_classes=()
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),

    path('api/v1/auth/', include("apps.accounts.urls")),
    path('api/v1/dashboard/', include("apps.dashboard.urls")),
    path('api/v1/accounts/', include("apps.accounts.router")),
    path('api/v1/address/', include("apps.address.urls")),
    path('api/v1/billings/', include("apps.billings.urls")),

    path('api/v1/outlets/', include("apps.outlets.urls")),
    path('api/v1/products/', include("apps.products.urls")),
    path('api/v1/upload/', include("apps.upload.urls")),
    path('api/v1/reports/', include("apps.reports.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
