from django.db import models

from apps.helpers.models import CreatedModel, UUIDModel

LINK_MAX_LEN = 127


class Channel(UUIDModel, CreatedModel):
    link = models.CharField('Ссылка на канал', max_length=LINK_MAX_LEN, unique=True)
    is_active = models.BooleanField('Парсинг активен', default=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Канал для парсинга'
        verbose_name_plural = 'Каналы для парсинга'

    def __str__(self):
        return self.link
