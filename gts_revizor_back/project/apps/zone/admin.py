from django.contrib import admin

from apps.task.models import Task
from apps.zone.models import Zone


class TaskAdminInline(admin.StackedInline):
    extra = 0
    model = Task


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'project',
        'storage_name',
        'serial_number',
        'code',
        'status',
        'is_auto_assignment',
        'created_at',
        'id',
    )
    fields = ('serial_number', 'code', 'title', 'status', 'project', 'storage_name', 'is_auto_assignment')
    list_filter = ('project',)
    inlines = (TaskAdminInline,)
