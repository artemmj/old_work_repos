from django.contrib import admin

from apps.template.models import TemplateEquipment, TemplateEquipmentDetail


@admin.register(TemplateEquipment)
class TemplateEquipmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_enable')


@admin.register(TemplateEquipmentDetail)
class TemplateEquipmentDetailAdmin(admin.ModelAdmin):
    list_display = ('id',)
