from django.db import models

from apps.helpers.models import UUIDModel


class TemplateVideo(UUIDModel):
    is_enable = models.BooleanField('Вкл/Выкл', default=True)
    order = models.PositiveIntegerField('Порядок', default=1)

    class Meta:
        verbose_name = 'Настройка видео'
        verbose_name_plural = 'Настройки видео'
