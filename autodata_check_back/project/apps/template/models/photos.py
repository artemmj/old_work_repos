from django.db import models

from apps.helpers.models import UUIDModel


class TemplatePhotosDetail(UUIDModel):
    front = models.BooleanField('Автомобиль в фас', default=True)
    front_left_three_quarters = models.BooleanField('Автомобиль ¾ спереди слева', default=True)
    front_left_wheel = models.BooleanField('Переднее левое колесо', default=True)
    front_right_wheel = models.BooleanField('Переднее правое колесо', default=True)
    front_right_three_quarters = models.BooleanField('Автомобиль ¾ спереди справа', default=True)
    front_seats = models.BooleanField('Передний ряд сидений', default=True)

    back = models.BooleanField('Автомобиль сзади', default=True)
    back_left_wheel = models.BooleanField('Заднее левое колесо', default=True)
    back_left_three_quarters = models.BooleanField('Автомобиль ¾ сзади слева', default=True)
    back_right_three_quarters = models.BooleanField('Автомобиль ¾ сзади справа', default=True)
    back_right_wheel = models.BooleanField('Заднее правое колесо', default=True)
    back_seats = models.BooleanField('Задний ряд сидений', default=True)

    left_side = models.BooleanField('Автомобиль сбоку слева', default=True)
    right_side = models.BooleanField('Автомобиль сбоку справа', default=True)

    open_trunk = models.BooleanField('Открытый багажник', default=True)
    steering = models.BooleanField('Руль крупно', default=True)
    torpedo = models.BooleanField('Торпедо крупно', default=True)
    back_seats_view = models.BooleanField('Вид на панель со второго ряда', default=True)
    under_hood = models.BooleanField('Под капотом', default=True)
    additional = models.BooleanField('Дополнительные фотографии', default=True)

    class Meta:
        verbose_name = 'Подробная настройка фотографий'
        verbose_name_plural = 'Подробные настройки фотографий'


class TemplatePhotos(UUIDModel):
    is_enable = models.BooleanField('Вкл/Выкл', default=True)
    detail = models.OneToOneField(
        TemplatePhotosDetail,
        verbose_name='Подробная настройка фотографий',
        related_name='template_photos',
        on_delete=models.CASCADE,
    )
    order = models.PositiveIntegerField('Порядок', default=1)

    class Meta:
        verbose_name = 'Настройка фотографий'
        verbose_name_plural = 'Настройки фотографий'
