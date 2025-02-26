from constance import config
from django.utils.timezone import now
from rest_framework import status
from rest_framework.exceptions import ValidationError

from apps.user.models import ConfirmationCode


def checking_code(phone, code):
    if not ConfirmationCode.objects.filter(phone=phone).exists():
        raise ValidationError({'phone': [config.CONFIRM_CODE_PHONE_NOT_FOUND_ERROR]}, code=status.HTTP_404_NOT_FOUND)

    confirmation_code = ConfirmationCode.objects.filter(phone=phone).latest('created_at')

    if code != confirmation_code.code:
        raise ValidationError({'code': [config.CONFIRM_CODE_INCORRECT_ERROR]})
    if now() > confirmation_code.expired_datetime:
        raise ValidationError({'code': [config.CONFIRM_CODE_EXPIRED_ERROR]}, code=status.HTTP_410_GONE)
