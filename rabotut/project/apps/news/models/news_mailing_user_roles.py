from django.db import models

from apps.helpers.models import ChoiceArrayField, enum_max_length
from apps.news.models import BaseNewsMailing, UserRolesChoices


class NewsMailingUserRole(BaseNewsMailing):
    roles = ChoiceArrayField(
        models.CharField(
            'Роль',
            max_length=enum_max_length(UserRolesChoices),
            choices=UserRolesChoices.choices,
        ),
        verbose_name='Роли',
    )

    class Meta(BaseNewsMailing.Meta):
        verbose_name = 'Новостная рассылка по ролям'
        verbose_name_plural = 'Новостные рассылки по ролям'
