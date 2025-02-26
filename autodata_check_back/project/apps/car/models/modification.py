from typing import Final

from bulk_update_or_create import BulkUpdateOrCreateQuerySet
from django.db import models

from apps.car.models import BodyTypeChoices, DriveTypeChoices, EngineTypeChoices, GearboxTypeChoices
from apps.car.models.brand import Brand
from apps.car.models.generation import Generation
from apps.car.models.model import Model
from apps.helpers.models import CreatedModel, UUIDModel, enum_max_length

_FIELD_MAX_LENGTH: Final = 100


class Modification(UUIDModel, CreatedModel):
    outer_id = models.IntegerField('Внешний ID', blank=True, null=True)
    title = models.CharField('Название модификации', max_length=_FIELD_MAX_LENGTH, default='', blank=True)
    brand = models.ForeignKey(
        Brand,
        verbose_name='Марка',
        related_name='modifications',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    model = models.ForeignKey(
        Model,
        verbose_name='Модель',
        related_name='modifications',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    generation = models.ForeignKey(
        Generation,
        verbose_name='Поколение',
        related_name='modifications',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    year_start = models.PositiveIntegerField('Год начала', blank=True, null=True)
    year_end = models.PositiveIntegerField('Год окончания', blank=True, null=True)
    body_type = models.CharField(
        'Тип кузова',
        max_length=enum_max_length(BodyTypeChoices),
        choices=BodyTypeChoices.choices,
        null=True,
        blank=True,
    )
    gearbox_type = models.CharField(
        'Тип коробки передач',
        max_length=enum_max_length(GearboxTypeChoices),
        choices=GearboxTypeChoices.choices,
        null=True,
        blank=True,
    )
    drive_type = models.CharField(
        'Тип привода',
        max_length=enum_max_length(DriveTypeChoices),
        choices=DriveTypeChoices.choices,
        null=True,
        blank=True,
    )
    engine_type = models.CharField(
        'Тип двигателя',
        max_length=enum_max_length(EngineTypeChoices),
        choices=EngineTypeChoices.choices,
        null=True,
        blank=True,
    )
    engine_volume = models.PositiveSmallIntegerField('Объем двигателя, см³', null=True, blank=True)
    engine_power = models.PositiveSmallIntegerField('Мощность двигателя, л/с', null=True, blank=True)

    objects = BulkUpdateOrCreateQuerySet.as_manager()    # noqa: WPS110

    class Meta:
        verbose_name = 'Модификация транспортного средства'
        verbose_name_plural = 'Модификации транспортных средств'

    def __str__(self):
        return f'{self.title}'
