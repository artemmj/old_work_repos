from django.db import models

from apps.helpers.models import DefaultModel, enum_max_length
from apps.news.models import EmojiChoices, News
from apps.user.models import User


class NewsEmoji(DefaultModel):
    news = models.ForeignKey(
        News,
        verbose_name='Новость',
        related_name='news_emoji',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='news_emoji',
        on_delete=models.CASCADE,
    )
    emoji_type = models.CharField(
        'Тип эмодзи',
        max_length=enum_max_length(EmojiChoices),
        choices=EmojiChoices,
    )

    class Meta:
        verbose_name = 'Эмодзи новости'
        verbose_name_plural = 'Эмодзи новостей'
        constraints = [
            models.UniqueConstraint(
                fields=['news', 'user'],
                name='Эмодзи юзера на новость',
            ),
        ]

    def __str__(self):
        return self.emoji_type
