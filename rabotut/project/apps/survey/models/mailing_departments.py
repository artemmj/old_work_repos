from django.db import models

from apps.departments.models import Department

from .mailing_base import BaseSurveyMailing


class SurveyMailingDepartments(BaseSurveyMailing):
    departments = models.ManyToManyField(Department, related_name='survey_mailings', verbose_name='Департаменты')

    class Meta(BaseSurveyMailing.Meta):
        verbose_name = 'Рассылка опросов по департаментам'
        verbose_name_plural = 'Рассылки опросов по департаментам'
