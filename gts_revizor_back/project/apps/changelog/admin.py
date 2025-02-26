from django.contrib import admin

from apps.changelog.models import ChangeLog


@admin.register(ChangeLog)
class ChangeLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'project', 'model', 'action_on_model', 'changed_data')
    list_filter = ('project', 'model', 'action_on_model')
    ordering = ('-created_at',)
