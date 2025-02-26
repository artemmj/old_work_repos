from django.contrib.auth import get_user_model
from django.db import models

from apps.helpers.models import DefaultModel, enum_max_length
from apps.promotion.models.promotion import Promotion

from .ext import EmojiChoices

User = get_user_model()


class PromotionEmoji(DefaultModel):
    promotion = models.ForeignKey(Promotion, models.CASCADE, related_name='promotion_emoji', verbose_name='Акция')
    user = models.ForeignKey(User, models.CASCADE, related_name='promotion_emoji', verbose_name='Пользователь')
    emoji_type = models.CharField('Тип эмодзи', max_length=enum_max_length(EmojiChoices), choices=EmojiChoices)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Эмодзи акций'
        verbose_name_plural = 'Эмодзи акций'
        constraints = [
            models.UniqueConstraint(
                fields=['promotion', 'user'],
                name='Эмодзи юзера на акцию',
            ),
        ]
