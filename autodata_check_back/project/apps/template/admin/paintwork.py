from django.contrib import admin

from apps.template.models import TemplatePaintwork


@admin.register(TemplatePaintwork)
class TemplatePaintworkAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_enable')
