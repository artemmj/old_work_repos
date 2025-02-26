from django.contrib import admin

from apps.template.models import TemplateTechnical


@admin.register(TemplateTechnical)
class TemplateTechnicalAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_enable')
