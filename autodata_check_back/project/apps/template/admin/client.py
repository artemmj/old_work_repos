from django.contrib import admin

from apps.template.models import TemplateClient


@admin.register(TemplateClient)
class TemplateClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_enable')
