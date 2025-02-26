from django.contrib import admin

from apps.document.models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'fake_id',
        'status',
        'color',
        'zone',
        'employee',
        'start_audit_date',
        'end_audit_date',
        'terminal',
        'created_at',
        'counter_scan_task',
        'controller_task',
        'auditor_task',
        'auditor_controller_task',
        'auditor_external_task',
        'storage_task',
    )
    list_filter = ('status', 'zone__project')
    raw_id_fields = (
        'employee',
        'zone',
        'counter_scan_task',
        'controller_task',
        'auditor_task',
        'auditor_controller_task',
        'auditor_external_task',
        'storage_task',
    )
    readonly_fields = ('color_changed', 'is_replace_specification')
