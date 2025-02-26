from django.db import models

from apps.departments.models import Department
from apps.stories.models import BaseStoriesMailing


class StoriesMailingDepartment(BaseStoriesMailing):
    departments = models.ManyToManyField(
        Department,
        related_name='stories_mailing',
        verbose_name='Департаменты',
    )

    class Meta(BaseStoriesMailing.Meta):
        verbose_name = 'Рассылка сторис по департаментам'
        verbose_name_plural = 'Рассылки сторис по департаментам'
