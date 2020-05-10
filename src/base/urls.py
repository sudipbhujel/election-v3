from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from accounts.models import upload_storage
from base import settings
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('election/', include('election.urls'))
]

if settings.DEBUG:
    urlpatterns += static(upload_storage.base_url,
                          document_root=upload_storage.location)
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
