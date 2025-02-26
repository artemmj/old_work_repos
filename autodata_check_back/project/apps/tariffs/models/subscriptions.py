from django.core.validators import MinValueValidator
from django.db import models

from apps.helpers.models import CreatedModel, UUIDModel


class Subscription(UUIDModel, CreatedModel):
    tariff = models.ForeignKey(
        'tariffs.Tariff',
        verbose_name='Тариф',
        related_name='subscriptions',
        on_delete=models.PROTECT,
    )
    organization = models.ForeignKey(
        'organization.Organization',
        verbose_name='Организация',
        related_name='subscriptions',
        on_delete=models.PROTECT,
    )
    amount = models.DecimalField(
        'Стоимость',
        max_digits=19,  # noqa: WPS432
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    is_active = models.BooleanField('Вкл/Выкл')
    auto_renewal = models.BooleanField('Автопродление')
    start_datetime = models.DateTimeField('Дата и время начала')
    end_datetime = models.DateTimeField('Дата и время окончания')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['organization'],
                condition=models.Q(is_active=True),
                name='unique_org_subs_active',
            ),
            models.UniqueConstraint(
                fields=['tariff', 'organization'],
                name='unique_tariff_org_subs',
            ),
        ]

    def __str__(self):
        return f'Подписка по тарифу {self.tariff.title} для организации {self.organization.title}'
