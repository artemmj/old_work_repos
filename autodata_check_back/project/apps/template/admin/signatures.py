from django.contrib import admin

from apps.template.models import TemplateSignatures


@admin.register(TemplateSignatures)
class TemplateSignaturesAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_enable')
