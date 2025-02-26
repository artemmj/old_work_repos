from django.contrib import admin

from apps.file.models import DBFile, File, Image, StaticFile


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    pass  # noqa: WPS420 WPS604


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass  # noqa: WPS420 WPS604


@admin.register(DBFile)
class DBFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'created_at')


@admin.register(StaticFile)
class StaticFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'created_at')
