from typing import Final

from django.contrib.gis.db.models import PointField
from django.db import models

from apps.address.models import City
from apps.helpers.models import UUIDModel

_FIELD_MAX_LENGTH: Final = 150


class Address(UUIDModel):
    city = models.ForeignKey(
        City,
        verbose_name='город',
        related_name='places',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    title = models.CharField('Название', max_length=_FIELD_MAX_LENGTH)
    location = PointField(verbose_name='Координаты')

    class Meta:
        ordering = ('title',)
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'

    def __str__(self):
        return self.title

    def longitude(self):
        return self.location.x

    def latitude(self):
        return self.location.y

    longitude.short_description = 'Долгота'
    latitude.short_description = 'Широта'
