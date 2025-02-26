from typing import Final

from django.db import models
from django_lifecycle import LifecycleModelMixin
from polymorphic.models import PolymorphicModel

from apps.helpers.models import CreatedModel, UUIDModel, enum_max_length


class NotificationStatuses(models.TextChoices):
    VIEWED = 'viewed', 'Просмотренное'
    NEW = 'new', 'Новое'


class BaseNotification(LifecycleModelMixin, CreatedModel, UUIDModel, PolymorphicModel):
    user = models.ForeignKey(
        'user.User',
        verbose_name='Пользователь',
        related_name='notifications',
        on_delete=models.CASCADE,
    )
    message = models.TextField('Сообщение')
    status = models.CharField(
        'Статус',
        max_length=enum_max_length(NotificationStatuses),
        choices=NotificationStatuses.choices,
        default=NotificationStatuses.NEW,
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Базовое уведомление'
        verbose_name_plural = 'Базовые уведомления'

    def __str__(self):
        return str(self.id)
