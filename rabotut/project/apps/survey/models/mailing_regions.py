from django.db import models

from apps.regions.models import Region

from .mailing_base import BaseSurveyMailing


class SurveyMailingRegions(BaseSurveyMailing):
    regions = models.ManyToManyField(Region, related_name='survey_mailings', verbose_name='Департаменты')
    to_all_regions = models.BooleanField('Рассылка на все регионы', null=True, blank=True)

    class Meta(BaseSurveyMailing.Meta):
        verbose_name = 'Рассылка опросов по регионам'
        verbose_name_plural = 'Рассылки опросов по регионам'
