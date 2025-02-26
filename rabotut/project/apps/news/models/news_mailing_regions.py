from django.db import models

from apps.news.models import BaseNewsMailing
from apps.regions.models import Region


class NewsMailingRegion(BaseNewsMailing):
    regions = models.ManyToManyField(Region, related_name='news_mailing', verbose_name='Регионы')
    to_all_regions = models.BooleanField('Рассылка на все регионы', null=True, blank=True)

    class Meta(BaseNewsMailing.Meta):
        verbose_name = 'Новостная рассылка по регионам'
        verbose_name_plural = 'Новостные рассылки по регионам'
