from apps.notification.models import BaseNotification


class OrganizationAddBalanceNotification(BaseNotification):
    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Уведомление о пополнении баланса организации'
        verbose_name_plural = 'Уведомления о пополнении баланса организации'

    def __str__(self):
        return str(self.id)
