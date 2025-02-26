from django.db import models

from apps.departments.models import Department
from apps.news.models import BaseNewsMailing


class NewsMailingDepartment(BaseNewsMailing):
    departments = models.ManyToManyField(
        Department,
        related_name='news_mailing',
        verbose_name='Департаменты',
    )

    class Meta(BaseNewsMailing.Meta):
        verbose_name = 'Новостная рассылка по департаментам'
        verbose_name_plural = 'Новостные рассылки по департаментам'
