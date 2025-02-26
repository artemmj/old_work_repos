from django.db import models

from apps.file.models import File, Image
from apps.helpers.consts import CHAR_FIELD_MIDDLE_LENGTH
from apps.helpers.models import DefaultModel, enum_max_length

from .ext import PromotionType


class Promotion(DefaultModel):
    end_date = models.DateTimeField('Дата окончания', null=True, blank=True)
    name = models.CharField('Название', max_length=CHAR_FIELD_MIDDLE_LENGTH)
    text = models.TextField('Текст')
    preview_standart = models.ForeignKey(
        Image,
        models.CASCADE,
        related_name='preview_standart_promotion',
        verbose_name='Превью стандарт',
    )
    preview_main = models.ForeignKey(
        Image,
        models.CASCADE,
        related_name='preview_main_promotion',
        verbose_name='Превью для главной',
        blank=True,
        null=True,
    )
    attachments = models.ManyToManyField(File, related_name='promotions', verbose_name='Вложения')
    type = models.CharField('Тип', max_length=enum_max_length(PromotionType), choices=PromotionType.choices)
    is_top = models.BooleanField('Закрепленная акция', default=False)
    is_main_display = models.BooleanField('Отображать на главной', default=False)
    is_hidden = models.BooleanField('Скрыть', default=False)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'

    def __str__(self):
        return self.name
