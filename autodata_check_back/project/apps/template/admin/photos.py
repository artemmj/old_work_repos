from django.contrib import admin

from apps.template.models import TemplatePhotos, TemplatePhotosDetail


@admin.register(TemplatePhotos)
class TemplatePhotosAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_enable')


@admin.register(TemplatePhotosDetail)
class TemplatePhotosDetailAdmin(admin.ModelAdmin):
    list_display = ('id',)
