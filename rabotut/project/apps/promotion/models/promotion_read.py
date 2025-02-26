from django.contrib.auth import get_user_model
from django.db import models

from apps.helpers.models import DefaultModel

from .promotion import Promotion

User = get_user_model()


class PromotionRead(DefaultModel):
    promotion = models.ForeignKey(Promotion, models.CASCADE, related_name='promotion_reads', verbose_name='Акция')
    user = models.ForeignKey(User, models.CASCADE, related_name='promotion_reads', verbose_name='Пользователь')

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'Просмотренная акция'
        verbose_name_plural = 'Просмотренные акции'
        constraints = [
            models.UniqueConstraint(fields=['promotion', 'user'], name='Просмотр юзером акции'),
        ]
