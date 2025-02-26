from django.db import models

from apps.projects.models import Project

from .mailing_base import BasePromotionMailing


class PromotionMailingProject(BasePromotionMailing):
    projects = models.ManyToManyField(Project, related_name='mailings', verbose_name='Проекты')

    class Meta(BasePromotionMailing.Meta):
        verbose_name = 'Рассылка акций по проектам'
        verbose_name_plural = 'Рассылки акций по проектам'
