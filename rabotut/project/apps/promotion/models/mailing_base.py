from django.db import models
from django.utils import timezone
from polymorphic.models import PolymorphicModel

from apps.helpers.models import DefaultModel
from apps.promotion.models.promotion import Promotion


class BasePromotionMailing(PolymorphicModel, DefaultModel):
    publish_datetime = models.DateTimeField('Время публикации', default=timezone.now)
    promotion = models.ForeignKey(Promotion, models.CASCADE, related_name='mailings', verbose_name='Акция')
    is_published = models.BooleanField('Опубликовано', default=False)
    is_push = models.BooleanField('Отправка пуша', default=False)

    class Meta:
        ordering = ('-created_at',)
