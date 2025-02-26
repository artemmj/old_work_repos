import types
from hashlib import md5
from uuid import uuid4

import httpx
import structlog
from django.conf import settings

from apps.helpers.services import AbstractService

API_URL = 'https://cp.redsms.ru/api/message'
ROUTE_TYPES = types.MappingProxyType({'sms': 'sms', 'viber': 'viber'})

log = structlog.get_logger()


class RedSmsService(AbstractService):
    def __init__(  # noqa: WPS211
        self,
        phone: str,
        message: str,
        route: str = 'sms',
        login: str | None = None,
        api_key: str | None = None,
    ) -> None:
        self.phone = phone
        self.message = message
        self.route = route

        if login is None:
            self.login = settings.RED_SMS_LOGIN

        if api_key is None:
            self.api_key = settings.RED_API_KEY

        action = 'Отправка сообщения через RedSms'
        self.log = log.bind(action=action, phone=self.phone, message=self.message, route=self.route)

    def process(self) -> bool:
        """Отправка sms сообщений через api redsms https://cp.redsms.ru/api-doc#post--api-message."""
        payload = {'route': ROUTE_TYPES.get(self.route, 'sms'), 'text': self.message, 'to': self.phone}
        headers = self.get_headers()
        try:
            response = httpx.post(API_URL, headers=headers, data=payload)
            response.raise_for_status()
        except httpx.HTTPError as e:
            self.log.error('Ошибка отправки сообщения', error=e)
            return False

        self.log.info('Успешная отправка сообщения')
        return True

    def get_headers(self):
        guid = str(uuid4())
        return {
            'Accept': 'application/json',
            'login': self.login,
            'ts': guid,
            'secret': md5(f'{guid}{self.api_key}'.encode()).hexdigest(),  # noqa: S324  Use of insecure hash function
        }
