from django.contrib import admin

from apps.terminal.models import Terminal


@admin.register(Terminal)
class TerminalAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'project',
        'number',
        'ip_address',
        'db_loading',
        'last_connect',
        'employee',
        'mac_address',
        'device_model',
    )
    list_filter = ('project__title', 'db_loading')
