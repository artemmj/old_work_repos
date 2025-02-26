from django.contrib import admin

from apps.template.models import Template, TemplateExport


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'field_separator', 'decimal_separator', 'fields')
    search_fields = ('title',)


@admin.register(TemplateExport)
class TemplateExportAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'field_separator',
        'decimal_separator',
        'fields',
        'zone_number_start',
        'zone_number_end',
        'is_products_find_by_code',
        'is_products_find_by_qr_code',
    )
    search_fields = ('title',)
