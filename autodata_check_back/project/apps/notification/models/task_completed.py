from django.db import models

from apps.notification.models import BaseNotification


class TaskCompletedNotification(BaseNotification):
    inspection_task = models.ForeignKey(
        'inspection_task.InspectionTask',
        verbose_name='Задание на осмотр',
        related_name='task_completed_notifications',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Уведомление о завершении задания'
        verbose_name_plural = 'Уведомления о завершении задания'

    def __str__(self):
        return str(self.id)
