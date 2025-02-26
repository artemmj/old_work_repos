from django.db import models

from apps.projects.models import Project
from apps.stories.models import BaseStoriesMailing


class StoriesMailingProject(BaseStoriesMailing):
    projects = models.ManyToManyField(
        Project,
        related_name='stories_mailing',
        verbose_name='Проекты',
    )

    class Meta(BaseStoriesMailing.Meta):
        verbose_name = 'Рассылка сторис по проектам'
        verbose_name_plural = 'Рассылки сторис по проектам'
