from typing import Final, final

from django.contrib.auth import models as auth_models
from django.db import models
from django_lifecycle import LifecycleModelMixin
from phonenumber_field.modelfields import PhoneNumberField

from apps.helpers.managers import CustomFieldUserManager
from apps.helpers.models import UUIDModel, enum_max_length

_FIELD_MAX_LENGTH: Final = 40


class UserRoles(models.TextChoices):
    EXAMPLE = 'role', 'роль'


@final
class User(LifecycleModelMixin, UUIDModel, auth_models.AbstractUser):
    username = models.CharField('Имя пользователя', max_length=_FIELD_MAX_LENGTH, default='', blank=True)
    first_name = models.CharField('Имя', max_length=_FIELD_MAX_LENGTH)
    middle_name = models.CharField('Отчество', max_length=_FIELD_MAX_LENGTH, default='', blank=True)
    last_name = models.CharField('Фамилия', max_length=_FIELD_MAX_LENGTH)
    phone = PhoneNumberField('Номер телефона', unique=True, help_text='Пример, +79510549236')
    email = models.EmailField('Адрес электронной почты', default='')
    role = models.CharField('Роль', max_length=enum_max_length(UserRoles), choices=UserRoles.choices)

    objects = CustomFieldUserManager(username_field_name='phone')  # noqa: WPS110

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'role']

    class Meta(auth_models.AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        ordering = ('email',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_username(self):
        # for jwt_payload_handler
        return str(self.phone)

    def __str__(self):
        return self.last_name
