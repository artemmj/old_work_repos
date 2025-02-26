from django.contrib import admin

from apps.template.models import TemplatePlace


@admin.register(TemplatePlace)
class TemplatePlaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_enable')
