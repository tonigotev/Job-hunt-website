from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('db_admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/companies/', include('companies.urls')),
    path('api/admins/', include('admins.urls')),
    path('api/seekers/', include('seekers.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
