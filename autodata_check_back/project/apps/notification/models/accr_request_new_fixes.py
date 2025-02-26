from django.db import models

from apps.notification.models import BaseNotification


class InspectorAccrNewFixesNotification(BaseNotification):
    accreditation_inspection = models.ForeignKey(
        'inspector_accreditation.AccreditationInspection',
        models.CASCADE,
        related_name='accr_new_fixes_notifications',
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Уведомление о том, что пришли корректировки по осмотру в заявке на аккредитию'
        verbose_name_plural = 'Уведомления о том, что пришли корректировки по осмотру в заявке на аккредитию'

    def __str__(self):
        return str(self.id)
