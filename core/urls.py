from django.contrib import admin
from django.urls import path

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = (
    [
        path("admin/", admin.site.urls),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)


admin.site.site_header = "Инструменты Виктории"
admin.site.index_title = "Инструменты Виктории"  # default: "Site administration"
admin.site.site_title = "Инструменты Виктории"  # default: "Django site admin"
admin.site.site_url = None
