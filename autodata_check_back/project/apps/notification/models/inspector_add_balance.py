from apps.notification.models import BaseNotification


class InspectorAddBalanceNotification(BaseNotification):
    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Уведомление о начислении инспектору за завершенное задание'
        verbose_name_plural = 'Уведомления о начислении инспектору за завершенное задание'

    def __str__(self):
        return str(self.id)
