from django.db import models

from apps.file.models import Image
from apps.helpers.consts import CHAR_FIELD_MIDDLE_LENGTH
from apps.helpers.models import DefaultModel


class Survey(DefaultModel):
    name = models.CharField('Название', max_length=CHAR_FIELD_MIDDLE_LENGTH)
    preview_standart = models.ForeignKey(
        Image,
        verbose_name='Стандартное превью',
        on_delete=models.CASCADE,
        related_name='preview_standart_survey',
    )
    preview_square = models.ForeignKey(
        Image,
        verbose_name='Квадратное превью',
        on_delete=models.CASCADE,
        related_name='preview_square_survey',
    )
    is_self_option = models.BooleanField(verbose_name='Свой вариант ответа')

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'
        ordering = ('-created_at',)

    def __str__(self):
        return self.name
