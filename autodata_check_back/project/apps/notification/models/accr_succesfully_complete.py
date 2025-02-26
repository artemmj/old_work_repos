from django.db import models

from apps.notification.models import BaseNotification


class InspectorAccrSuccCompleteNotification(BaseNotification):
    accreditation_inspection = models.ForeignKey(
        'inspector_accreditation.AccreditationInspection',
        models.CASCADE,
        related_name='accr_success_compl_notifications',
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Уведомление о том, что аккредитация успешно пройдена'
        verbose_name_plural = 'Уведомления о том, что аккредитация успешно пройдена'

    def __str__(self):
        return str(self.id)
