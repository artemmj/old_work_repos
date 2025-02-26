from django.db import models

from apps.projects.models import Project

from .mailing_base import BaseSurveyMailing


class SurveyMailingProjects(BaseSurveyMailing):
    projects = models.ManyToManyField(Project, related_name='survey_mailings', verbose_name='Проекты')

    class Meta(BaseSurveyMailing.Meta):
        verbose_name = 'Рассылка опросов по проектам'
        verbose_name_plural = 'Рассылки опросов по проектам'
