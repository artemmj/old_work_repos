from django.db import models

from apps.helpers.models import UUIDModel


class TemplateEquipmentDetail(UUIDModel):
    visibility = models.BooleanField('Обзор', default=True)
    exterior = models.BooleanField('Экстерьер', default=True)
    protection = models.BooleanField('Защита от угона', default=True)
    multimedia = models.BooleanField('Мультимедиа', default=True)
    salon = models.BooleanField('Салон', default=True)
    comfort = models.BooleanField('Комфорт', default=True)
    safety = models.BooleanField('Безопасность', default=True)
    other = models.BooleanField('Прочее', default=True)

    class Meta:
        verbose_name = 'Подробная настройка комплектации'
        verbose_name_plural = 'Подробные настройки комплектаций'


class TemplateEquipment(UUIDModel):
    is_enable = models.BooleanField('Вкл/Выкл', default=True)
    order = models.PositiveIntegerField('Порядок', default=1)
    detail = models.OneToOneField(
        TemplateEquipmentDetail,
        verbose_name='Подробная настройка комплектации',
        related_name='template_equipment',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Настройка комплектации'
        verbose_name_plural = 'Настройки комплектаций'
