from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path

admin.site.site_title = 'AutoData'
admin.site.site_header = 'AutoData'
admin.site.index_title = 'Панель администрирования'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(('api.v1.urls', 'api_v1'))),
    url('^ckeditor/', include('ckeditor_uploader.urls')),
]


if settings.DEBUG:
    from django.conf.urls.static import static  # noqa: WPS433

    urlpatterns += \
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
