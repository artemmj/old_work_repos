from django.contrib import admin

from apps.employee.models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('username', 'project', 'serial_number', 'roles', 'is_deleted', 'is_auto_assignment', 'id')
    list_filter = ('project',)
