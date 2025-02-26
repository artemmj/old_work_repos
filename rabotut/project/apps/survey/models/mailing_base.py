from django.db import models
from django.utils import timezone
from polymorphic.models import PolymorphicModel

from apps.helpers.models import DefaultModel

from .survey import Survey


class BaseSurveyMailing(PolymorphicModel, DefaultModel):
    publish_datetime = models.DateTimeField('Время публикации', default=timezone.now)
    survey = models.ForeignKey(Survey, verbose_name='Опрос', on_delete=models.CASCADE, related_name='mailings')
    is_published = models.BooleanField('Опубликовано', default=False)
    is_push = models.BooleanField('Отправка пуша', default=False)

    class Meta:
        ordering = ('-created_at',)
