from django.db import models

from apps.notification.models import BaseNotification


class TaskAcceptedNotification(BaseNotification):
    inspection_task = models.ForeignKey(
        'inspection_task.InspectionTask',
        verbose_name='Задание на осмотр',
        related_name='task_accepted_notifications',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Уведомление о принятии задания'
        verbose_name_plural = 'Уведомления о принятии задания'

    def __str__(self):
        return str(self.id)
