from typing import Dict

import httpx
import structlog
from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import ValidationError

logger = structlog.getLogger()

ERROR_STATUSES = {
    status.HTTP_400_BAD_REQUEST,
    status.HTTP_401_UNAUTHORIZED,
    status.HTTP_403_FORBIDDEN,
    status.HTTP_404_NOT_FOUND,
    status.HTTP_500_INTERNAL_SERVER_ERROR,
}
REQUEST_TIMEOUT = 30


class ArketaApiClient:
    def __init__(self, token: str):
        self.api_url = f'{settings.ARKETA_API_URL}api/v4/'
        self.client = httpx.Client()
        self.token = token

    def _request(self, method: str, url: str, payload: Dict = None, files: Dict = None):
        try:
            return self._make_request(method, url, payload=payload, files=files)
        except httpx.HTTPError as exc:
            raise ValidationError(f'ArketaApiError: Ошибка при взаимодействии с апи аркеты: {exc}')

    def _make_request(self, method: str, url: str, payload: Dict = None, files: Dict = None) -> Dict:
        request_params = {'url': url, 'timeout': REQUEST_TIMEOUT}
        if payload:
            request_params['data'] = payload
        if files:
            request_params['files'] = files
        response = getattr(self.client, method)(**request_params)
        json_response = response.json() if response.content else None
        if response.status_code in ERROR_STATUSES:
            logger.error(f'ArketaApiError: {method} {url} (status {response.status_code}) content: {json_response}')
            raise ValidationError(response.json().get('errors'))
        return json_response
