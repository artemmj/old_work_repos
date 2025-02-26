from django.db import models

from apps.helpers.models import UUIDModel


class TemplatePlace(UUIDModel):
    is_enable = models.BooleanField('Вкл/Выкл', default=True)
    order = models.PositiveIntegerField('Порядок', default=1)

    class Meta:
        verbose_name = 'Настройка места осмотра'
        verbose_name_plural = 'Настройки места осмотра'
