from constance import config
from django.db import models
from django_lifecycle import LifecycleModelMixin, hook
from rest_framework.exceptions import ValidationError

from apps.helpers.models import CreatedModel, UUIDModel, enum_max_length
from apps.transaction.models.abstract import Transaction, TransactionTypes


class InspectorTransactionOperations(models.TextChoices):
    COMPLETED_TASK = 'completed_task', 'Начисление за выполненное задание'   # noqa: WPS115
    WITHDRAW_TO_CARD = 'withdraw_to_card', 'Вывод средств на карту'   # noqa: WPS115


class InspectorTransaction(LifecycleModelMixin, UUIDModel, CreatedModel, Transaction):
    inspector = models.ForeignKey(
        'inspector.Inspector',
        verbose_name='Инспектор',
        related_name='transactions',
        on_delete=models.CASCADE,
    )
    operation = models.CharField(
        'Название операции',
        max_length=enum_max_length(InspectorTransactionOperations),
        choices=InspectorTransactionOperations.choices,
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Транзакция инспектора'
        verbose_name_plural = 'Транзакции инспектора'

    @hook('before_create')
    def validate_balance(self):
        if self.type == TransactionTypes.WITHDRAW and self.inspector.balance < self.amount:
            raise ValidationError({'error': config.INSPECTOR_TRANSACTION_INSUFFICIENT_FUNDS_ERROR})

    @hook('after_create')
    def execute_transaction(self):
        from apps.transaction.services.executor import TransactionExecutor  # noqa: WPS433, I001
        TransactionExecutor().execute(self.id)
