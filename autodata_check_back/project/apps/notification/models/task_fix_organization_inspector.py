from django.db import models

from apps.notification.models import BaseNotification


class TaskFixOrganizationInspectorNotification(BaseNotification):
    inspection_task = models.ForeignKey(
        'inspection_task.InspectionTask',
        verbose_name='Задание на осмотр',
        related_name='task_fix_organization_inspector_notifications',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Уведомление о правках в задании инспектору организации'
        verbose_name_plural = 'Уведомления о правках в задании инспектору организации'

    def __str__(self):
        return str(self.id)
