from django.db import models

from apps.helpers.models import UUIDModel


class TemplateCompleteness(UUIDModel):
    is_enable = models.BooleanField('Вкл/Выкл', default=True)
    order = models.PositiveIntegerField('Порядок', default=1)

    class Meta:
        verbose_name = 'Настройка комплектности'
        verbose_name_plural = 'Настройки комплектностей'
