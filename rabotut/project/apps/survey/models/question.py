from django.db import models

from apps.helpers.consts import CHAR_FIELD_SMALL_LENGTH
from apps.helpers.models import DefaultModel

from .survey import Survey


class Question(DefaultModel):
    name = models.CharField('Вопрос', max_length=CHAR_FIELD_SMALL_LENGTH)
    survey = models.ForeignKey(Survey, verbose_name='Опрос', on_delete=models.CASCADE, related_name='questions')
    number = models.SmallIntegerField('Порядковый номер')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ('-created_at',)

    def __str__(self):
        return self.name
