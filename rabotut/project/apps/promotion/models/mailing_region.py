from django.db import models

from apps.regions.models import Region

from .mailing_base import BasePromotionMailing


class PromotionMailingRegion(BasePromotionMailing):
    regions = models.ManyToManyField(Region, related_name='mailings', verbose_name='Департаменты')
    to_all_regions = models.BooleanField('Рассылка на все регионы', null=True, blank=True)

    class Meta(BasePromotionMailing.Meta):
        verbose_name = 'Рассылка акций по регионам'
        verbose_name_plural = 'Рассылки акций по регионам'
