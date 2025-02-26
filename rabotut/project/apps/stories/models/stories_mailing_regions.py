from django.db import models

from apps.regions.models import Region
from apps.stories.models import BaseStoriesMailing


class StoriesMailingRegion(BaseStoriesMailing):
    regions = models.ManyToManyField(Region, related_name='stories_mailing', verbose_name='Регионы')
    to_all_regions = models.BooleanField('Рассылка на все регионы', null=True, blank=True)

    class Meta(BaseStoriesMailing.Meta):
        verbose_name = 'Рассылка сторис по регионам'
        verbose_name_plural = 'Рассылки сторис по регионам'
