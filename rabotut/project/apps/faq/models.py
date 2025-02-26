from django.db import models

from apps.helpers.consts import CHAR_FIELD_MIDDLE_LENGTH
from apps.helpers.models import DefaultModel


class Faq(DefaultModel):
    title = models.CharField(verbose_name='Заголовок', max_length=CHAR_FIELD_MIDDLE_LENGTH)
    body = models.TextField(verbose_name='Содержание')

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Часто задаваемый вопрос'
        verbose_name_plural = 'Часто задаваемые вопросы'
