from django.db import models

from apps.departments.models import Department

from .mailing_base import BasePromotionMailing


class PromotionMailingDepartment(BasePromotionMailing):
    departments = models.ManyToManyField(Department, related_name='mailings', verbose_name='Департаменты')

    class Meta(BasePromotionMailing.Meta):
        verbose_name = 'Рассылка акций по департаментам'
        verbose_name_plural = 'Рассылки акций по департаментам'
