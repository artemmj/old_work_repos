import re

from constance import config
from rest_framework.exceptions import ValidationError


def agreement_validator(data):  # noqa: D103, WPS110
    if data.__contains__('agreement_processing') and data.__contains__('agreement_policy'):  # noqa: WPS609
        if data['agreement_processing'] is False:
            raise ValidationError(config.AGREEMENT_PROCESSING_NEED_ERROR)

        if data['agreement_policy'] is False:
            raise ValidationError(config.AGREEMENT_POLICY_NEED_ERROR)


def username_validator(data):  # noqa: D103, WPS110
    if data.get('last_name') and not re.search(r'^[А-Я-а-я]*\Z', data['last_name']):
        raise ValidationError({'last_name': ['Поле должно содержать буквы русского алфавита']})

    if data.get('first_name') and not re.search(r'^[А-Я-а-я]*\Z', data['first_name']):
        raise ValidationError({'first_name': ['Поле должно содержать буквы русского алфавита']})

    if data.get('middle_name') and not re.search(r'^[А-Я-а-я]*\Z', data['middle_name']):
        raise ValidationError({'middle_name': ['Поле должно содержать буквы русского алфавита']})
