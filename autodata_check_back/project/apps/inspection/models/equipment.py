from django.contrib.postgres.fields import JSONField
from django.db import models
from django_lifecycle import LifecycleModelMixin

from apps.car.models.car import Car
from apps.helpers.models import CreatedModel, UUIDModel
from apps.inspection.mixins import InspectionUpdateDateMixin
from apps.inspection.models.inspection import Inspection


class Equipment(LifecycleModelMixin, InspectionUpdateDateMixin, UUIDModel, CreatedModel):
    inspection = models.OneToOneField(
        Inspection,
        verbose_name='Осмотр',
        related_name='equipment',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    accreditation_inspection = models.OneToOneField(
        'inspector_accreditation.AccreditationInspection',
        verbose_name='Осмотр на аккредитацию',
        related_name='equipment',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    answer = JSONField('Ответ на экран', default=dict)

    class Meta:
        verbose_name = 'Комплектация автомобиля'
        verbose_name_plural = 'Комплектации автомобилей'

    def __str__(self):
        if Car.objects.filter(inspection=self.inspection).exists():
            car_inspection = Car.objects.filter(inspection=self.inspection).first()
            return f'{car_inspection}'
        return str(self.id)
