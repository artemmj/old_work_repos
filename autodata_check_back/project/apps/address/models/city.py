from typing import Final

from django.contrib.gis.db.models import PointField
from django.db import models

_FIELD_MAX_LENGTH: Final = 150


class City(models.Model):
    fias_id = models.UUIDField('fias_id', primary_key=True, editable=False)
    title = models.CharField('Название', max_length=_FIELD_MAX_LENGTH)
    location = PointField(verbose_name='Координаты центра')
    inspection_price = models.DecimalField(
        'Цена за осмотр',
        max_digits=19,   # noqa: WPS432
        decimal_places=2,
        default='100.00',
    )

    class Meta:
        ordering = ('title',)
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.title

    def longitude(self):
        return self.location.x

    def latitude(self):
        return self.location.y

    longitude.short_description = 'Долгота'
    latitude.short_description = 'Широта'
