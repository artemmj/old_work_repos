from datetime import datetime, timedelta
from typing import Final

from constance import config
from django.db import models
from django.utils.timezone import now
from django_lifecycle import LifecycleModelMixin, hook
from phonenumber_field.modelfields import PhoneNumberField

from apps.helpers.models import CreatedModel, UUIDModel
from apps.helpers.sms import SmsAPI, gen_code

_FIELD_MAX_LENGTH: Final = 40


def calculate_expired_datetime():
    return now() + timedelta(minutes=config.CONFIRMATION_CODE_EXPIRED_TIME)


class ConfirmationCode(LifecycleModelMixin, UUIDModel, CreatedModel):
    phone = PhoneNumberField('Номер телефона', help_text='Пример, +79510549236')
    code = models.CharField('Код', max_length=4, default=gen_code, editable=False)
    expired_datetime = models.DateTimeField(
        'Дата и время окончания жизни кода',
        default=calculate_expired_datetime,
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Код подтверждения'
        verbose_name_plural = 'Коды подтверждения'

    @hook('after_create')
    def after_create(self):
        SmsAPI().send_sms(f'Код подтверждения:{self.code}', str(self.phone))
