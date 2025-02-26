import urllib
from typing import Dict

from .api_client import ArketaApiClient


class ArketaFeedbackApiClient(ArketaApiClient):
    def __init__(self, token: str):
        super().__init__(token)
        self.client.headers = {'Authorization': self.token}

    def create(self, serializer_data: Dict):
        url = f'{self.api_url}feedback/'
        return self._request('post', url, payload=serializer_data)

    def notifications(self, serializer_data: Dict):
        query_params = {}
        if 'unread_exists' in serializer_data and serializer_data.get('unread_exists'):
            query_params['unread_exists'] = serializer_data.get('unread_exists')
        if 'search' in serializer_data:
            query_params['search'] = serializer_data.get('search')
        if 'limit' in serializer_data:
            query_params['limit'] = serializer_data.get('limit')
        if 'offset' in serializer_data:
            query_params['offset'] = serializer_data.get('offset')
        url = f'{self.api_url}feedback/notifications/?{urllib.parse.urlencode(query_params)}'
        return self._request('get', url)

    def show_to_executor(self, feedback_id: str):
        url = f'{self.api_url}feedback/{feedback_id}/show_to_executor/'
        return self._request('post', url)
