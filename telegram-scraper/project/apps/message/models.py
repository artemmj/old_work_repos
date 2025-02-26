from django.db import models

from apps.channel.models import Channel
from apps.helpers.models import CreatedModel, UUIDModel


class Message(UUIDModel, CreatedModel):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='messages', verbose_name='Канал')
    ext_id = models.PositiveIntegerField('Айди в телеграме')
    ext_date = models.DateTimeField('Время публикации поста', null=True, blank=True)
    text = models.TextField('Текстовое сообщение', null=True, blank=True)
    link = models.URLField('Ссылка на сообщение', null=True, blank=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Пост/Сообщение'
        verbose_name_plural = 'Посты/Сообщения'
