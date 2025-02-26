import urllib
from typing import Dict, List

import structlog

from .api_client import ArketaApiClient

logger = structlog.getLogger()


class ArketaTaskApiClient(ArketaApiClient):  # noqa: WPS214
    def __init__(self, token: str):
        super().__init__(token)
        self.client.headers = {'Authorization': self.token}

    def task_vacant(self, serializer_data: Dict):
        """Задачи торговой точки."""
        self.client.headers.pop('Authorization')
        query_params = {
            'distance__latitude': serializer_data.get('latitude'),
            'distance__longitude': serializer_data.get('longitude'),
        }
        if 'trade_point' in serializer_data:
            query_params['trade_point'] = ','.join(serializer_data.get('trade_point'))
        if 'limit' in serializer_data:
            query_params['limit'] = serializer_data.get('limit')
        if 'is_liked' in serializer_data:
            query_params['is_liked'] = serializer_data.get('is_liked')

        url = f'{self.api_url}task/vacant/?{urllib.parse.urlencode(query_params)}'
        return self._request('get', url)

    def task_available_for_reserve(self):
        """Показывает, забронировал пользователь максимально разрешенное количество задач или нет."""
        url = f'{self.api_url}task/available_for_reserve/'
        return self._request('get', url)

    def task_preview(self, task_id: str):
        """Просмотр задачи перед бронированием."""
        url = f'{self.api_url}task/{task_id}/preview/'
        return self._request('get', url)

    def vacant_take(self, tasks: List[str], collection: str = None):
        """Бронирование/взятие задач исполнителем."""
        url = f'{self.api_url}task/vacant/take/'
        payload = {'tasks': tasks}
        if collection:
            payload['collection'] = collection
        return self._request('post', url, payload=payload)

    def check_arketa_documents(self):
        """Роут статусов документов пользователя в аркете."""
        url = f'{self.api_url}task/check_docs/'
        return self._request('get', url)

    def statuses(self):
        """Роут со списком кол-ва задач разбитых по статусам."""
        url = f'{self.api_url}task/statuses/'
        return self._request('get', url)

    def current(self, serializer_data: Dict):
        """Роут с задачами пользователя."""
        query_params = {}
        if 'latitude' in serializer_data:
            query_params['latitude'] = serializer_data.get('latitude')
        if 'longitude' in serializer_data:
            query_params['longitude'] = serializer_data.get('longitude')
        if 'status' in serializer_data:
            query_params['status'] = serializer_data.get('status')
        if 'ordering' in serializer_data:
            query_params['ordering'] = serializer_data.get('ordering')
        url = f'{self.api_url}task/current/?{urllib.parse.urlencode(query_params)}'
        return self._request('get', url)

    def cancel_reservation(self, task_id: str, payload: Dict):
        """Отмена бронирования/отказ от задачи."""
        url = f'{self.api_url}task/{task_id}/cancel_reservation/'
        return self._request('post', url, payload=payload)

    def answer(self, payload: Dict):
        """Отправка ответов."""
        url = f'{self.api_url}task/answer/'
        return self._request('post', url, payload=payload)

    def visit(self, payload: Dict):
        """Фиксация визита."""
        url = f'{self.api_url}visit/'
        return self._request('post', url, payload=payload)

    def like(self, task_id: str):
        """Добавить задачу в избранное."""
        url = f'{self.api_url}task/{task_id}/like/'
        return self._request('post', url)

    def dislike(self, task_id: str):
        """Удалить задачу из избранного."""
        url = f'{self.api_url}task/{task_id}/dislike/'
        return self._request('post', url)
