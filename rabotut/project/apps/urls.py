from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.urls import path

admin.site.site_title = 'RABOTUT'
admin.site.site_header = 'RABOTUT'
admin.site.index_title = 'Панель администрирования'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(('api.v1.urls', 'api_v1'))),
    path('ckeditor5/', include('django_ckeditor_5.urls'), name='ck_editor_5_upload_file'),
]

if settings.DEBUG:
    from django.conf.urls.static import static  # noqa: WPS433

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
