from django.contrib import admin

from apps.transaction.models import InspectorTransaction, OrganizationTransaction


@admin.register(OrganizationTransaction)
class OrganizationTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'type', 'operation', 'created_at', 'organization')
    raw_id_fields = ('organization', 'user')
    list_filter = ('status', 'type', 'operation', 'organization')
    date_hierarchy = 'created_at'
    readonly_fields = ('status',)

    # def has_delete_permission(self, request, obj=None):
    #     return False   # noqa: E800

    def has_change_permission(self, request, obj=None):   # noqa: WPS110
        return False


@admin.register(InspectorTransaction)
class InspectorTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'type', 'operation', 'created_at')
    raw_id_fields = ('inspector',)
    list_filter = ('status', 'type', 'operation')
    date_hierarchy = 'created_at'
    readonly_fields = ('status',)

    # def has_delete_permission(self, request, obj=None):
    #     return False   # noqa: E800

    def has_change_permission(self, request, obj=None):   # noqa: WPS110
        return False
