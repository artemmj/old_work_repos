from django.contrib import admin

from apps.template.models import TemplateCompleteness


@admin.register(TemplateCompleteness)
class TemplateCompletenessAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_enable')
