from django.db import models
from django.utils import timezone
from polymorphic.models import PolymorphicModel

from apps.helpers.models import DefaultModel


class BaseStoriesMailing(PolymorphicModel, DefaultModel):
    stories = models.ForeignKey(
        'Stories',
        related_name='stories_mailing',
        verbose_name='Сторис',
        on_delete=models.PROTECT,
    )
    publish_datetime = models.DateTimeField('Дата публикации', default=timezone.now)
    is_published = models.BooleanField('Опубликовано', default=False)
    is_push = models.BooleanField('Отправка пуш-уведомления', default=False)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Базовая рассылка сторис'
        verbose_name_plural = 'Базовые рассылки сторис'

    def __str__(self):
        return self.stories.name
