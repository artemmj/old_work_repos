from typing import Final

from bulk_update_or_create import BulkUpdateOrCreateQuerySet
from django.db import models

from apps.car.models.brand import Brand
from apps.car.models.category import Category
from apps.car.models.model import Model
from apps.helpers.models import CreatedModel, UUIDModel

_FIELD_MAX_LENGTH: Final = 100


class Generation(UUIDModel, CreatedModel):
    outer_id = models.IntegerField('Внешний ID', blank=True, null=True)
    title = models.CharField('Название поколения', max_length=_FIELD_MAX_LENGTH, default='', blank=True, null=True)
    category = models.ForeignKey(
        Category,
        verbose_name='Тип ТС',
        related_name='generations',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    brand = models.ForeignKey(
        Brand,
        verbose_name='Марка',
        related_name='generations',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    model = models.ForeignKey(
        Model,
        verbose_name='Модель',
        related_name='generations',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    year_start = models.PositiveIntegerField('Год начала поколения', blank=True, null=True)
    year_end = models.PositiveIntegerField('Год окончания поколения', blank=True, null=True)

    objects = BulkUpdateOrCreateQuerySet.as_manager()    # noqa: WPS110

    class Meta:
        verbose_name = 'Поколение транспорного средства'
        verbose_name_plural = 'Поколения транспортных средств'

    def __str__(self):
        return f'{self.year_start}-{self.year_end} {self.title}'
