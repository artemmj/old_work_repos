from django.contrib import admin

from apps.template.models import TemplateLift


@admin.register(TemplateLift)
class TemplateLiftAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_enable')
