from typing import Final

from bulk_update_or_create import BulkUpdateOrCreateQuerySet
from django.db import models

from apps.file.models import Image
from apps.helpers.models import CreatedModel, UUIDModel

_FIELD_MAX_LENGTH: Final = 100


class Brand(UUIDModel, CreatedModel):
    outer_id = models.IntegerField('Внешний ID', blank=True, null=True)
    title = models.CharField('Название марки', max_length=_FIELD_MAX_LENGTH)
    popular = models.BooleanField('Популярная марка', default=False)
    logo = models.ForeignKey(
        Image,
        verbose_name='Логотип',
        related_name='brands',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    objects = BulkUpdateOrCreateQuerySet.as_manager()    # noqa: WPS110

    class Meta:
        verbose_name = 'Марка транспорного средства'
        verbose_name_plural = 'Марки транспортных средств'
        ordering = ['title']

    def __str__(self):
        return f' {self.title}'
