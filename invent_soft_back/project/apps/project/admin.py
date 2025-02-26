from django.contrib import admin

from apps.project.models import Project, RMMSettings, TerminalSettings


class TerminalSettingsInline(admin.StackedInline):
    extra = 0
    model = TerminalSettings

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class RMMSettingsInline(admin.StackedInline):
    extra = 0
    model = RMMSettings

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'address',
        'created_at',
        'accounting_without_yk',
        'auto_assign_enbale',
    )
    search_fields = ('title',)
    fieldsets = (
        (None, {'fields': ('title', 'address', 'manager', 'template', 'accounting_without_yk', 'auto_assign_enbale')}),
    )
    inlines = (RMMSettingsInline, TerminalSettingsInline)


@admin.register(TerminalSettings)
class TerminalSettingsAdmin(admin.ModelAdmin):
    list_display = (
        'project',
        'issuing_task',
        'length_barcode_pallets',
        'error_correction',
        'product_name',
        'unknown_barcode',
        'trimming_barcode',
        'recalculation_discrepancy',
        'suspicious_barcodes_amount',
        'check_dm',
        'check_am',
        'search_by_product_code',
        'password',
    )


@admin.register(RMMSettings)
class RMMSettingsAdmin(admin.ModelAdmin):
    list_display = (
        'project',
        'auto_zones_amount',
        'password',
        'norm',
        'extended_tasks',
    )
