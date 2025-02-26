from django.core.validators import MinValueValidator
from django.db import models

from apps.helpers.models import enum_max_length


class TransactionStatuses(models.TextChoices):
    PENDING = 'pending', 'Ожидание'  # noqa: WPS115
    ERROR = 'error', 'Ошибка'  # noqa: WPS115
    DONE = 'done', 'Завершена'  # noqa: WPS115


class TransactionTypes(models.TextChoices):
    ADD = 'add', 'Начисление'  # noqa: WPS115
    WITHDRAW = 'withdraw', 'Списание'  # noqa: WPS115


class Transaction(models.Model):
    status = models.CharField(
        'Статус',
        max_length=enum_max_length(TransactionStatuses),
        choices=TransactionStatuses.choices,
        default=TransactionStatuses.PENDING,
    )
    type = models.CharField(
        'Тип',
        max_length=enum_max_length(TransactionTypes),
        choices=TransactionTypes.choices,
    )
    amount = models.DecimalField(
        'Сумма транзакции',
        max_digits=19,  # noqa: WPS432
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    class Meta:
        abstract = True
