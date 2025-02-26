from django.db import models
from django.utils import timezone
from polymorphic.models import PolymorphicModel

from apps.helpers.models import DefaultModel


class BaseNewsMailing(PolymorphicModel, DefaultModel):
    news = models.ForeignKey(
        'News',
        related_name='news_mailing',
        verbose_name='Новость',
        on_delete=models.PROTECT,
    )
    publish_datetime = models.DateTimeField('Дата публикации', default=timezone.now)
    is_published = models.BooleanField('Опубликовано', default=False)
    is_push = models.BooleanField('Отправка пуш-уведомления', default=False)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Базовая рассылка новостей'
        verbose_name_plural = 'Базовые рассылки новостей'

    def __str__(self):
        return self.news.name
