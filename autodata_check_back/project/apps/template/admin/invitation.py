from django.contrib import admin

from apps.template.models import TemplateInvitation


@admin.register(TemplateInvitation)
class TemplateInvitationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'template', 'status')
