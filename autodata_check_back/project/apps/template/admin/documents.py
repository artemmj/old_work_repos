from django.contrib import admin

from apps.template.models import TemplateDocuments, TemplateDocumentsDetail


@admin.register(TemplateDocuments)
class TemplateDocumentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_enable')


@admin.register(TemplateDocumentsDetail)
class TemplateDocumentsDetailAdmin(admin.ModelAdmin):
    list_display = ('id',)
