from django.db import models

from apps.helpers.models import ChoiceArrayField, enum_max_length

from .ext import UserRolesChoices
from .mailing_base import BasePromotionMailing


class PromotionMailingUserRole(BasePromotionMailing):
    roles = ChoiceArrayField(
        models.CharField('Роль', max_length=enum_max_length(UserRolesChoices), choices=UserRolesChoices.choices),
        verbose_name='Роли',
    )

    class Meta(BasePromotionMailing.Meta):
        verbose_name = 'Рассылка акций по ролям'
        verbose_name_plural = 'Рассылки акций по ролям'
