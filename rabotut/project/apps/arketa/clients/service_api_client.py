import logging
import urllib
from typing import Dict

import httpx
from django.conf import settings
from rest_framework import status

from apps.user.models import User

logger = logging.getLogger()

ERROR_STATUSES = {
    status.HTTP_400_BAD_REQUEST,
    status.HTTP_401_UNAUTHORIZED,
    status.HTTP_403_FORBIDDEN,
    status.HTTP_404_NOT_FOUND,
    status.HTTP_500_INTERNAL_SERVER_ERROR,
}


class ArketaServiceApiClient:  # noqa: WPS214
    client = httpx.Client()
    client.headers = {'X-API-KEY': settings.ARKETA_X_API_KEY}
    api_url = f'{settings.ARKETA_API_URL}api/v4/'

    def create_user(self, user: User):
        """Создание юзера в аркете."""
        url = f'{self.api_url}rabotut/user/registration/'
        payload = {
            'id': user.id,
            'phone': str(user.phone),
            'inn': user.inn.non_deleted().first().value,
            'last_name': user.last_name,
            'first_name': user.first_name,
            'middle_name': user.middle_name,
        }
        return self._request('post', url, payload=payload)

    def change_user_phone(self, user_id: str, phone: str):
        """Изменить номер телефона пользователя в аркете."""
        url = f'{self.api_url}rabotut/user/{user_id}/phone/'
        payload = {'phone': phone}
        return self._request('post', url, payload=payload)

    def check_user_exists(self, phone: str):
        """Проверить наличие юзера в аркете по номеру телефона."""
        check_phone_url = f'{self.api_url}rabotut/user/exists/?'
        check_phone_url += urllib.parse.urlencode({'phone': phone})
        return self._request('get', check_phone_url)

    def get_documents(self, user_id: str):
        """Получить инфо о статусах документов юзера."""
        documents_url = f'{self.api_url}rabotut/document/user/{user_id}/documents/'
        return self._request('get', documents_url)

    def put_bank_detail(self, user_id: str, payload: Dict):
        """TODO Изменить данные банковской карты юзера."""
        bank_detail_url = f'{self.api_url}rabotut/document/user/{user_id}/bank_detail/'
        return self._request('put', bank_detail_url, payload=payload)

    def put_email(self, user_id: str, payload: Dict):
        """Изменить данные эл. почты."""
        email_url = f'{self.api_url}rabotut/document/user/{user_id}/email/'
        return self._request('put', email_url, payload=payload)

    def put_inn(self, user_id: str, payload: Dict):
        """Изменить данные ИНН."""
        inn_url = f'{self.api_url}rabotut/document/user/{user_id}/inn/'
        return self._request('put', inn_url, payload=payload)

    def put_registration(self, user_id: str, payload: Dict):
        """Изменить данные страницы с регистрацией."""
        registration_url = f'{self.api_url}rabotut/document/user/{user_id}/registration/'
        return self._request('put', registration_url, payload=payload)

    def put_selfie(self, user_id: str, payload: Dict):
        """Изменить данные селфи с паспортом."""
        selfie_url = f'{self.api_url}rabotut/document/user/{user_id}/selfie/'
        return self._request('put', selfie_url, payload=payload)

    def put_snils(self, user_id: str, payload: Dict):
        """Изменить данные СНИЛС."""
        snils_url = f'{self.api_url}rabotut/document/user/{user_id}/snils/'
        return self._request('put', snils_url, payload=payload)

    def put_spread(self, user_id: str, payload: Dict):
        """Изменить данные разворота паспорта."""
        spread_url = f'{self.api_url}rabotut/document/user/{user_id}/spread/'
        return self._request('put', spread_url, payload=payload)

    def _request(self, method: str, url: str, payload: Dict = None) -> Dict:
        request_params = {'url': url}
        if method in {'post', 'put', 'patch'}:
            request_params['data'] = payload
        try:
            response = getattr(self.client, method)(**request_params)
            if response.status_code in ERROR_STATUSES:
                code = response.status_code
                resp_content = response.content.decode('utf-8') if response.content else ''
                logger.error(f'ArketaServiceApiError: {method} {url} (status {code}) content: {resp_content}')
            return response.json()
        except httpx.HTTPError as exc:
            logger.error(f'ArketaServiceApiError: Ошибка при взаимодействии с апи аркеты: {exc}')
