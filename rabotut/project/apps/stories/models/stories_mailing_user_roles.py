from django.db import models

from apps.helpers.models import ChoiceArrayField, enum_max_length
from apps.news.models import UserRolesChoices
from apps.stories.models import BaseStoriesMailing


class StoriesMailingUserRole(BaseStoriesMailing):
    roles = ChoiceArrayField(
        models.CharField(
            'Роль',
            max_length=enum_max_length(UserRolesChoices),
            choices=UserRolesChoices.choices,
        ),
        verbose_name='Роли',
    )

    class Meta(BaseStoriesMailing.Meta):
        verbose_name = 'Рассылка сторис по ролям'
        verbose_name_plural = 'Рассылки сторис по ролям'
