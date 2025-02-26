from django.db import models

from apps.file.models import Image
from apps.helpers.consts import CHAR_FIELD_MIDDLE_LENGTH, CHAR_FIELD_SMALL_LENGTH
from apps.helpers.models import DefaultModel
from apps.news.models import News


class Stories(DefaultModel):
    name = models.CharField('Название', max_length=CHAR_FIELD_MIDDLE_LENGTH)
    preview = models.ForeignKey(Image, verbose_name='Превью', related_name='preview_stories', on_delete=models.CASCADE)
    slides = models.ManyToManyField(Image, verbose_name='Слайды', related_name='slides_stories', blank=True)
    news = models.ForeignKey(
        News,
        verbose_name='Новости',
        related_name='stories',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    background_color_button = models.CharField('Цвет кнопки', max_length=CHAR_FIELD_SMALL_LENGTH, blank=True, null=True)
    text_color = models.CharField('Цвет текста', max_length=CHAR_FIELD_SMALL_LENGTH, blank=True, null=True)
    text_button = models.CharField('Текст кнопки', max_length=CHAR_FIELD_SMALL_LENGTH, blank=True, null=True)
    is_top = models.BooleanField('Закрепленная сторис', default=False)

    class Meta:
        verbose_name = 'Сторис'
        verbose_name_plural = 'Сторисы'

    def __str__(self):
        return self.name
