from django.contrib import admin

from apps.template.models import Template


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'is_active', 'is_main', 'is_accreditation')
    search_fields = ('title',)
