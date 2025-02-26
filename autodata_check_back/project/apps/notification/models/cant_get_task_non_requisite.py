from django.db import models

from apps.notification.models import BaseNotification


class CantGetTaskWithoutRequisiteNotification(BaseNotification):
    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Уведомление о том, что невозможно получить задание без заполненных реквизитов'
        verbose_name_plural = 'Уведомления о том, что невозможно получить задание без заполненных реквизитов'

    def __str__(self):
        return str(self.id)
