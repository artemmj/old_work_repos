from django.db import models

from apps.helpers.models import DefaultModel
from apps.news.models import News
from apps.user.models import User


class NewsRead(DefaultModel):
    news = models.ForeignKey(
        News,
        verbose_name='Новость',
        related_name='news_read',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='news_read',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Просмотренная новость'
        verbose_name_plural = 'Просмотренные новости'
        constraints = [
            models.UniqueConstraint(
                fields=['news', 'user'],
                name='Просмотр новости пользователем',
            ),
        ]

    def __str__(self):
        return self.news.name
