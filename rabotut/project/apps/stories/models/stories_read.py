from django.db import models

from apps.helpers.models import DefaultModel
from apps.stories.models import Stories
from apps.user.models import User


class StoriesRead(DefaultModel):
    stories = models.ForeignKey(
        Stories,
        verbose_name='Сторис',
        related_name='stories_read',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='stories_read',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Просмотренная сторис'
        verbose_name_plural = 'Просмотренные сторисы'
        constraints = [
            models.UniqueConstraint(
                fields=['stories', 'user'],
                name='Просмотр сторис пользователем',
            ),
        ]

    def __str__(self):
        return self.stories.name
