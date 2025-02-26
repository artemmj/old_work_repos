from django.contrib import admin

from apps.file.models import File, Image


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'file')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass  # noqa: WPS420 WPS604
