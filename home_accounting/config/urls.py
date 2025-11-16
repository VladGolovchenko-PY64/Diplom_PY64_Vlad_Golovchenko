# home_accounting/config/urls.py
from django.contrib import admin
from django.urls import path, include
from apps.core.views import index
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", index, name="home"),
    path("admin/", admin.site.urls),

    # HTML-шаблоны
    path("users/", include("apps.users.urls_template", namespace="users_template")),  # страницы регистрации/логина
    path("finance/", include("apps.finance.urls_template", namespace="finance")),
    path("reports/", include("apps.reports.urls", namespace="reports")),

    # API
    path("api/users/", include("apps.users.urls", namespace="users_api")),  # DRF API
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
