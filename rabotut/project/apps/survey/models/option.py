from django.db import models

from apps.helpers.consts import CHAR_FIELD_SMALL_LENGTH
from apps.helpers.models import DefaultModel

from .question import Question


class Option(DefaultModel):
    name = models.CharField('Название', max_length=CHAR_FIELD_SMALL_LENGTH)
    question = models.ForeignKey(Question, verbose_name='Вопрос', on_delete=models.CASCADE, related_name='options')
    number = models.SmallIntegerField('Порядковый номер')

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответов'
        ordering = ('-created_at',)

    def __str__(self):
        return self.name
