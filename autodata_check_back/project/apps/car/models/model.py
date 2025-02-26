from typing import Final

from bulk_update_or_create import BulkUpdateOrCreateQuerySet
from django.db import models

from apps.car.models.brand import Brand
from apps.car.models.category import Category
from apps.helpers.models import CreatedModel, UUIDModel

_FIELD_MAX_LENGTH: Final = 100


class Model(UUIDModel, CreatedModel):
    outer_id = models.IntegerField('Внешний ID', blank=True, null=True)
    title = models.CharField('Название модели', max_length=_FIELD_MAX_LENGTH)
    category = models.ForeignKey(
        Category,
        verbose_name='Тип ТС',
        related_name='models',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    brand = models.ForeignKey(
        Brand,
        verbose_name='Марка',
        related_name='models',
        on_delete=models.PROTECT,
    )
    year_start = models.PositiveIntegerField('Год начала', blank=True, null=True)
    year_end = models.PositiveIntegerField('Год окончания', blank=True, null=True)
    popular = models.BooleanField('Популярная модель', default=False)

    objects = BulkUpdateOrCreateQuerySet.as_manager()    # noqa: WPS110

    class Meta:
        verbose_name = 'Модель транспорного средства'
        verbose_name_plural = 'Модели транспортных средств'

    def __str__(self):
        return f'{self.title}'
