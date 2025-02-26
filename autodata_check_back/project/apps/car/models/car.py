from typing import Final

from django.db import models
from django_lifecycle import LifecycleModelMixin

from apps.car.models import BodyTypeChoices, DriveTypeChoices, EngineTypeChoices, GearboxTypeChoices
from apps.car.models.brand import Brand
from apps.car.models.category import Category
from apps.car.models.generation import Generation
from apps.car.models.model import Model
from apps.car.models.modification import Modification
from apps.helpers.models import CreatedModel, UUIDModel, enum_max_length
from apps.inspection.models.inspection import Inspection

_FIELD_MAX_LENGTH: Final = 40
_FIELD_LENGTH_GOVNUMBER: Final = 13


class Car(LifecycleModelMixin, UUIDModel, CreatedModel):
    vin_code = models.CharField('VIN-код', max_length=17)   # noqa: WPS432
    unstandart_vin = models.BooleanField('Нестандартный VIN', default=False)
    gov_number = models.CharField('Гос.номер', max_length=_FIELD_LENGTH_GOVNUMBER, null=True, blank=True)
    category = models.ForeignKey(
        Category,
        verbose_name='Тип ТС',
        related_name='cars',
        on_delete=models.PROTECT,
    )
    brand = models.ForeignKey(
        Brand,
        verbose_name='Марка',
        related_name='cars',
        on_delete=models.PROTECT,
    )
    model = models.ForeignKey(
        Model,
        verbose_name='Модель',
        related_name='cars',
        on_delete=models.PROTECT,
    )
    generation = models.ForeignKey(
        Generation,
        verbose_name='Поколение',
        related_name='cars',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
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
    modification = models.ForeignKey(
        Modification,
        verbose_name='Модификация',
        related_name='cars',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    color = models.CharField('Цвет', max_length=_FIELD_MAX_LENGTH, null=True, blank=True)
    mileage = models.FloatField('Пробег', null=True, blank=True)
    mileage_unknown = models.BooleanField('Пробег не установлен', default=False)
    engine_volume = models.FloatField('Объем двигателя, см³', null=True, blank=True)
    engine_power = models.FloatField('Мощность двигателя, л.с.', null=True, blank=True)
    production_year = models.PositiveIntegerField('Год выпуска', null=True, blank=True)
    inspection = models.OneToOneField(
        Inspection,
        verbose_name='Осмотр',
        related_name='car',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    accreditation_inspection = models.OneToOneField(
        'inspector_accreditation.AccreditationInspection',
        verbose_name='Осмотр на аккредитацию',
        related_name='car',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'

    def __str__(self):
        return f'{self.brand.title} {self.model.title} {self.vin_code}'  # noqa: WPS237, WPS221
