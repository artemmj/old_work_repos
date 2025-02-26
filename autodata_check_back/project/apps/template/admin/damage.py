from django.contrib import admin

from apps.template.models import TemplateDamage


@admin.register(TemplateDamage)
class TemplateDamageAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_enable')
