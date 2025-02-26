from django.contrib.gis.db.models import PointField
from django.db import models

from apps.helpers.consts import CHAR_FIELD_MIDDLE_LENGTH
from apps.helpers.models import DefaultModel
from apps.regions.models import Region


class City(DefaultModel):
    name = models.CharField('Название', max_length=CHAR_FIELD_MIDDLE_LENGTH)
    location = PointField('Местоположение')
    region = models.ForeignKey(Region, models.CASCADE, verbose_name='Регион', related_name='cities')

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ('created_at',)

    def __str__(self):
        return self.name
