from django.contrib import admin

from apps.template.models import TemplateVideo


@admin.register(TemplateVideo)
class TemplateVideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_enable')
