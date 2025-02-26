from typing import Final, final

from django.contrib.auth import models as auth_models
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from apps.helpers.managers import CustomFieldUserManager
from apps.helpers.models import UUIDModel

_FIELD_MAX_LENGTH: Final = 40


@final
class User(UUIDModel, auth_models.AbstractUser):
    username = models.CharField('Имя пользователя', max_length=_FIELD_MAX_LENGTH, default='', blank=True)
    phone = PhoneNumberField('Номер телефона', unique=True, help_text='Пример, +79510549236')
    first_name = models.CharField('Имя', max_length=_FIELD_MAX_LENGTH, null=True, blank=True)
    middle_name = models.CharField('Отчество', max_length=_FIELD_MAX_LENGTH, null=True, blank=True)
    last_name = models.CharField('Фамилия', max_length=_FIELD_MAX_LENGTH, null=True, blank=True)

    objects = CustomFieldUserManager(username_field_name='phone')  # noqa: WPS110

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['last_name', 'first_name', 'middle_name']

    class Meta(auth_models.AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        ordering = ('phone',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_username(self):
        # for jwt_payload_handler
        return str(self.phone)

    def __str__(self):
        return str(self.phone)
