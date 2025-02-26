from django.db import models

from apps.notification.models import BaseNotification


class TaskInvitationNotification(BaseNotification):
    inspection_task_invitation = models.ForeignKey(
        'inspection_task.Invitation',
        verbose_name='Приглашение по заданию',
        related_name='task_inspector_notifications',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Уведомление о приглашении по заданию'
        verbose_name_plural = 'Уведомления о приглашениях по заданию'

    def __str__(self):
        return str(self.id)
