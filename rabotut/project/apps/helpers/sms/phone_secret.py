import random
import string

import structlog
from constance import config
from django.core.cache import cache
from rest_framework.exceptions import ValidationError

from apps.helpers.services import AbstractService

PHONE_CODE_KEY = 'phone_code:{phone}'
PHONE_SECRET_KEY = 'phone_secret:{phone}'
SIMPLE_CODE_LENGTH = 6
COUNTER_KEY = 'daily_code_count:{phone}'

log = structlog.get_logger()


class PhoneSecretService(AbstractService):  # noqa: WPS214
    """Верификация номера телефона и действий пользователя."""

    def __init__(self):
        self.log = log.bind(action='Создание короткого кода для авторизации')

    def process(self, phone: str) -> dict:
        """Генерация кода и проверка счетчика."""
        self.daily_counter(phone=phone)

        if self.is_send_code(phone=phone):
            self.log.warning('Превышен лимит создания кодов для авторизации.', phone=phone)
            raise ValidationError('Превышен лимит попыток авторизации.')

        code = cache.get(PHONE_CODE_KEY.format(phone=phone))
        if not code:
            code = self.create_code(phone)
        message = f'Код для проверки телефона: {code}'
        return {
            'phone': phone,
            'code': code if config.SMS_CODE_IN_RESPONSE else '',
            'message': message,
        }

    @staticmethod
    def daily_counter(phone: str) -> None:
        """Увеличение счетчика."""
        if not cache.get(COUNTER_KEY.format(phone=phone)):
            cache.set(COUNTER_KEY.format(phone=phone), 0, config.PHONE_CODE_COUNTER_TTL)
        cache.incr(COUNTER_KEY.format(phone=phone))

    @classmethod
    def is_send_code(cls, phone: str) -> bool:
        """Проверка счетчика."""
        return cls.get_counter_value(phone=phone) > config.COUNT_SEND_SMS

    @staticmethod
    def get_counter_value(phone: str) -> int:
        """Получение значения счетчика."""
        return cache.get(COUNTER_KEY.format(phone=phone))

    @staticmethod
    def create_code(phone: str) -> str:
        """Создание кода для проверки номера телефона."""
        code = ''.join(random.choices(string.digits, k=SIMPLE_CODE_LENGTH))  # noqa: S311
        cache.set(PHONE_CODE_KEY.format(phone=phone), code, config.PHONE_CODE_KEY_TTL)
        return code

    @staticmethod
    def is_valid_code(phone: str, code: str) -> bool:
        """Валидация пары: номер телефона + код."""
        return code == cache.get(PHONE_CODE_KEY.format(phone=phone))

    @staticmethod
    def clear(phone: str) -> None:
        """Очистка кода и секрета по номеру телефона."""
        code = PHONE_CODE_KEY.format(phone=phone)
        secret = PHONE_SECRET_KEY.format(phone=phone)
        cache.delete_many([code, secret])
