from django.db import models

from apps.file.models import File, Image
from apps.helpers.consts import CHAR_FIELD_MIDDLE_LENGTH
from apps.helpers.models import DefaultModel


class News(DefaultModel):
    name = models.CharField('Название', max_length=CHAR_FIELD_MIDDLE_LENGTH)
    text = models.TextField('Текст')
    preview_standard = models.ForeignKey(
        Image,
        verbose_name='Превью стандарт',
        related_name='preview_standard_news',
        on_delete=models.CASCADE,
    )
    preview_main = models.ForeignKey(
        Image,
        verbose_name='Превью для главной',
        related_name='preview_main_news',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    attachments = models.ManyToManyField(
        File,
        verbose_name='Вложения',
        related_name='news',
        blank=True,
    )
    is_top = models.BooleanField('Закрепленная новость', default=False)
    is_main_page = models.BooleanField('Отображать на главной', default=False)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.name
