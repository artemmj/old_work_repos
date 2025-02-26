from constance import config  # noqa: WPS402
from django.db import models
from django_lifecycle import LifecycleModelMixin, hook
from rest_framework.exceptions import ValidationError

from apps.devices.tasks import send_push
from apps.helpers.models import CreatedModel, UUIDModel, enum_max_length
from apps.notification.models import OrganizationAddBalanceNotification
from apps.transaction.models.abstract import Transaction, TransactionStatuses, TransactionTypes
from apps.transaction.services.pay_request import PayRequestService


class OrganizationTransactionOperations(models.TextChoices):
    BALANCE_REPLENISHMENT = 'balance_replenishment', 'Пополнение баланса'  # noqa: WPS115
    HAND_BALANCE_REPLENISHMENT = 'hand_balance_replenishment', 'Ручное зачисление в баланс'  # noqa: WPS115
    HAND_BALANCE_WITHDRAW = 'hand_balance_withdraw', 'Ручное списание с баланса'  # noqa: WPS115
    SELF_INSPECTION = 'self_inspection', 'Списание за самостоятельный осмотр'  # noqa: WPS115
    INSPECTION_TASK = 'inspection_task', 'Списание за задание на осмотр'  # noqa: WPS115
    REFUND_CANCELED_TASK = 'refund_canceled_task', 'Возврат за отмененное задание'  # noqa: WPS115
    PAYMENT_TARIFF = 'payment_tariff', 'Оплата по тарифу'  # noqa: WPS115


class OrganizationTransaction(LifecycleModelMixin, UUIDModel, CreatedModel, Transaction):
    organization = models.ForeignKey(
        'organization.Organization',
        verbose_name='Организация',
        related_name='transactions',
        on_delete=models.PROTECT,
    )
    user = models.ForeignKey(
        'user.User',
        verbose_name='Пользователь',
        related_name='transactions',
        on_delete=models.PROTECT,
    )
    operation = models.CharField(
        'Название операции',
        max_length=enum_max_length(OrganizationTransactionOperations),
        choices=OrganizationTransactionOperations.choices,
    )
    payment_url = models.URLField('URL адреса страницы оплаты', null=True, blank=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Транзакция организации'
        verbose_name_plural = 'Транзакции организации'

    @hook('before_create')
    def validate_balance(self):
        if self.type == TransactionTypes.WITHDRAW and self.organization.balance < self.amount:
            raise ValidationError({'error': config.ORG_TRANSACTION_INSUFFICIENT_FUNDS_ERROR})

    @hook('after_create')
    def execute_transaction(self):
        if self.operation != OrganizationTransactionOperations.BALANCE_REPLENISHMENT:  # noqa: WPS504
            from apps.transaction.services.executor import TransactionExecutor  # noqa: WPS433, I001
            TransactionExecutor().execute(self.id)
        else:
            PayRequestService(self).process()

    @hook('after_update')
    def after_update(self):
        if (  # noqa: WPS337
            self.operation == OrganizationTransactionOperations.BALANCE_REPLENISHMENT
            and self.status == TransactionStatuses.DONE
        ):
            amount = '{0:,}'.format(round(self.amount, 0)).replace(',', ' ')  # noqa: WPS221
            message = config.ORGANIZATION_BALANCE_MONEY_CAME.replace('[ ]', f'+{amount}')
            notification = OrganizationAddBalanceNotification.objects.create(user=self.user, message=message)
            send_push.delay(
                str(self.user_id),
                message,
                {
                    'push_type': 'OrganizationAddBalanceNotification',
                    'notification_id': str(notification.id),
                },
            )
