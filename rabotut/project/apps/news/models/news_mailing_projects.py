from django.db import models

from apps.news.models import BaseNewsMailing
from apps.projects.models import Project


class NewsMailingProject(BaseNewsMailing):
    projects = models.ManyToManyField(
        Project,
        related_name='news_mailing',
        verbose_name='Проекты',
    )

    class Meta(BaseNewsMailing.Meta):
        verbose_name = 'Новостная рассылка по проектам'
        verbose_name_plural = 'Новостные рассылки по проектам'
