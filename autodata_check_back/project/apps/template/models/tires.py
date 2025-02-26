from django.db import models

from apps.helpers.models import UUIDModel


class TemplateTiresDetail(UUIDModel):
    additional = models.BooleanField('Дополнительный комплект', default=True)

    class Meta:
        verbose_name = 'Подробная настройка шин'
        verbose_name_plural = 'Подробные настройки шин'


class TemplateTires(UUIDModel):
    is_enable = models.BooleanField('Вкл/Выкл', default=True)
    detail = models.OneToOneField(
        TemplateTiresDetail,
        verbose_name='Подробная настройка шин',
        related_name='template_tires',
        on_delete=models.CASCADE,
    )
    order = models.PositiveIntegerField('Порядок', default=1)

    class Meta:
        verbose_name = 'Настройка шин'
        verbose_name_plural = 'Настройки шин'
