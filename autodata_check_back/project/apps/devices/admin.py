from django.contrib import admin
from fcm_django.admin import DeviceAdmin
from fcm_django.models import FCMDevice


class CustomDeviceAdmin(DeviceAdmin):
    list_filter = ('active', 'type')

admin.site.unregister(FCMDevice)  # noqa: E305
admin.site.register(FCMDevice, CustomDeviceAdmin)
