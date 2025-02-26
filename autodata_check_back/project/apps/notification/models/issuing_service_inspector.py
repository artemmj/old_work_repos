from django.db import models

from apps.notification.models import BaseNotification


class IssuingServiceInspectorNotification(BaseNotification):
    task = models.ForeignKey(
        'inspection_task.InspectionTask',
        on_delete=models.CASCADE,
        related_name='iss_service_inspector_notifications',
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Уведомление о получении осмотров инспектором сервиса'
        verbose_name_plural = 'Уведомления о получении осмотров инспектором сервиса'

    def __str__(self):
        return str(self.id)
