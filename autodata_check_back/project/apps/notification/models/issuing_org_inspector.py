from django.db import models

from apps.notification.models import BaseNotification


class IssuingOrganizationInspectorNotification(BaseNotification):
    task = models.ForeignKey(
        'inspection_task.InspectionTask',
        on_delete=models.CASCADE,
        related_name='iss_org_inspector_notifications',
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Уведомление о получении инспектором осмотров по заданию организации'
        verbose_name_plural = 'Уведомления о получении инспектором осмотров по заданию организации'

    def __str__(self):
        return str(self.id)
