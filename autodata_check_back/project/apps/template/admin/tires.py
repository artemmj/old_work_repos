from django.contrib import admin

from apps.template.models import TemplateTires, TemplateTiresDetail


@admin.register(TemplateTires)
class TemplateTiresAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_enable')


@admin.register(TemplateTiresDetail)
class TemplateTiresDetailAdmin(admin.ModelAdmin):
    list_display = ('id',)
