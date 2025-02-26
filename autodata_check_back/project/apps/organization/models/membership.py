from typing import Final

from django.db import models

from apps.helpers.models import CreatedModel, UUIDModel, enum_max_length
from apps.organization.models import Organization

_FIELD_MAX_LENGTH: Final = 150


class MembershipRoleChoices(models.TextChoices):
    OWNER = 'owner', 'Владелец'  # noqa: WPS115
    MANAGER = 'manager', 'Управляющий'  # noqa: WPS115
    INSPECTOR = 'inspector', 'Инспектор'  # noqa: WPS115


class Membership(UUIDModel, CreatedModel):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    role = models.CharField(
        'Роль участника организации',
        max_length=enum_max_length(MembershipRoleChoices),
        choices=MembershipRoleChoices.choices,
    )
    is_active = models.BooleanField('Активная организация пользователя', default=False)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Членство пользователя в организации'
        verbose_name_plural = 'Членства пользователей в организациях'
