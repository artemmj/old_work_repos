from typing import Final

from django.core.validators import MinValueValidator
from django.db import models

from apps.helpers.models import CreatedModel, UUIDModel, enum_max_length

TITLE_MAX_LENGTH: Final = 150
DESCRIPTION_MAX_LENGTH: Final = 500


class TariffPeriodChoices(models.TextChoices):
    WEEK = 'week', 'Неделя'
    MONTH = 'month', 'Месяц'
    HALF_YEAR = 'half_year', 'Полгода'
    YEAR = 'year', 'Год'


class Tariff(UUIDModel, CreatedModel):
    title = models.CharField('Заголовок', max_length=TITLE_MAX_LENGTH)
    subtitle = models.CharField('Подзаголовок', max_length=TITLE_MAX_LENGTH)
    description = models.CharField('Описание', max_length=DESCRIPTION_MAX_LENGTH)
    period = models.CharField(
        'Период',
        max_length=enum_max_length(TariffPeriodChoices),
        choices=TariffPeriodChoices.choices,
    )
    amount = models.DecimalField(
        'Стоимость',
        max_digits=19,  # noqa: WPS432
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    organization = models.ForeignKey(
        'organization.Organization',
        verbose_name='Организация',
        related_name='tariffs',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ('title',)
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'

    def __str__(self):
        return self.title
