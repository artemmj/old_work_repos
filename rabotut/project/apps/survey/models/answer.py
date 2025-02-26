from django.contrib.auth import get_user_model
from django.db import models

from apps.helpers.consts import CHAR_FIELD_MIDDLE_LENGTH
from apps.helpers.models import DefaultModel

from .option import Option
from .question import Question

User = get_user_model()


class Answer(DefaultModel):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, verbose_name='Вопрос', on_delete=models.CASCADE)
    options = models.ManyToManyField(Option, verbose_name='Варианты ответов', related_name='answers')
    self_option_answer = models.CharField(
        'Свой вариант ответа',
        max_length=CHAR_FIELD_MIDDLE_LENGTH,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        ordering = ('-created_at',)
