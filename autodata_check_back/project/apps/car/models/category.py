from typing import Final

from bulk_update_or_create import BulkUpdateOrCreateQuerySet
from django.db import models

from apps.helpers.models import CreatedModel, UUIDModel

_FIELD_MAX_LENGTH: Final = 40


class Category(UUIDModel, CreatedModel):
    outer_id = models.IntegerField('Внешний ID', blank=True, null=True)
    title = models.CharField('Название категории', max_length=_FIELD_MAX_LENGTH)

    objects = BulkUpdateOrCreateQuerySet.as_manager()    # noqa: WPS110

    class Meta:
        verbose_name = 'Тип ТС'
        verbose_name_plural = 'Типы ТС'

    def __str__(self):
        return f' {self.title}'
