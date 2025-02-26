from django.contrib import admin

from apps.notification.models import (  # noqa: WPS235
    InspectorAddBalanceNotification,
    IssuingOrganizationInspectorNotification,
    IssuingServiceInspectorNotification,
    OrganizationAddBalanceNotification,
    OrganizationInvitationNotification,
    TaskAcceptedNotification,
    TaskCompletedNotification,
    TaskFixOrganizationInspectorNotification,
    TaskFixServiceInspectorNotification,
    TaskInvitationNotification,
    TemplateInvitationNotification,
)


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'user', 'message', 'status')
    list_filter = ('user', 'status')


@admin.register(InspectorAddBalanceNotification)
class InspectorAddBalanceNotificationAdmin(NotificationAdmin):
    raw_id_fields = ('user',)


@admin.register(IssuingOrganizationInspectorNotification)
class IssuingOrganizationInspectorNotificationAdmin(NotificationAdmin):
    raw_id_fields = ('user',)


@admin.register(IssuingServiceInspectorNotification)
class IssuingServiceInspectorNotificationAdmin(NotificationAdmin):
    raw_id_fields = ('user',)


@admin.register(OrganizationAddBalanceNotification)
class OrganizationAddBalanceNotificationAdmin(NotificationAdmin):
    raw_id_fields = ('user',)


@admin.register(OrganizationInvitationNotification)
class OrganizationInvitationNotificationAdmin(NotificationAdmin):
    raw_id_fields = ('user', 'org_invitation')


@admin.register(TaskAcceptedNotification)
class TaskAcceptedNotificationAdmin(NotificationAdmin):
    raw_id_fields = ('user', 'inspection_task')


@admin.register(TaskCompletedNotification)
class TaskCompletedNotificationAdmin(NotificationAdmin):
    raw_id_fields = ('user', 'inspection_task')


@admin.register(TaskFixOrganizationInspectorNotification)
class TaskFixOrganizationInspectorNotificationAdmin(NotificationAdmin):
    raw_id_fields = ('user', 'inspection_task')


@admin.register(TaskFixServiceInspectorNotification)
class TaskFixServiceInspectorNotificationAdmin(NotificationAdmin):
    raw_id_fields = ('user', 'inspection_task')


@admin.register(TaskInvitationNotification)
class TaskInvitationNotificationAdmin(NotificationAdmin):
    raw_id_fields = ('user', 'inspection_task_invitation')


@admin.register(TemplateInvitationNotification)
class TemplateInvitationNotificationAdmin(NotificationAdmin):
    raw_id_fields = ('user', 'template_invitation')
