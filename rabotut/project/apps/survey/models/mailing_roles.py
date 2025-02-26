from django.db import models

from apps.helpers.models import ChoiceArrayField, enum_max_length

from .ext import UserRolesChoices
from .mailing_base import BaseSurveyMailing


class SurveyMailingRoles(BaseSurveyMailing):
    roles = ChoiceArrayField(
        models.CharField('Роль', max_length=enum_max_length(UserRolesChoices), choices=UserRolesChoices.choices),
        verbose_name='Роли',
    )

    class Meta(BaseSurveyMailing.Meta):
        verbose_name = 'Рассылка опросов по ролям'
        verbose_name_plural = 'Рассылки опросов по ролям'
