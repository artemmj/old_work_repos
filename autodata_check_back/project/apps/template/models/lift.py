from django.db import models

from apps.helpers.models import UUIDModel


class TemplateLift(UUIDModel):
    is_enable = models.BooleanField('Вкл/Выкл', default=True)
    order = models.PositiveIntegerField('Порядок', default=1)

    class Meta:
        verbose_name = 'Настройка осмотра на подъемнике'
        verbose_name_plural = 'Настройки осмотра на подъемнике'
