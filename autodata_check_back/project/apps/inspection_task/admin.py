from django.contrib import admin

from apps.inspection_task.models.invitation import Invitation
from apps.inspection_task.models.search import InspectionTaskSearch
from apps.inspection_task.models.task import InspectionTask, InspectionTaskCar


class InspectionTaskCarInline(admin.StackedInline):
    model = InspectionTaskCar
    extra = 0
    raw_id_fields = ('brand', 'model')


@admin.register(InspectionTask)
class InspectionTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'fio', 'start_date', 'end_date', 'status')
    inlines = (InspectionTaskCarInline,)
    raw_id_fields = ('author', 'inspector', 'organization', 'address')
    readonly_fields = ('status', 'is_accrual')


@admin.register(InspectionTaskSearch)
class InspectionTaskSearchAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'is_active')
    fieldsets = (
        (None, {'fields': ('task', 'level', 'start_time', 'start_time_iter', 'is_active')}),
    )
    readonly_fields = ('start_time', 'start_time_iter')


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    pass  # noqa: WPS420, WPS604
