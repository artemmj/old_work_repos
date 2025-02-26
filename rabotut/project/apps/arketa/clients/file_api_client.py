from typing import Dict

from .api_client import ArketaApiClient


class ArketaFileApiClient(ArketaApiClient):
    def __init__(self, token: str = None):
        super().__init__(token)
        if token:
            self.client.headers = {'Authorization': self.token}

    def create_file(self, serializer_data: Dict):
        url = f'{self.api_url}file/'
        return self._request('post', url, files={'file': serializer_data.get('file')})

    def get_file(self, file_id: str):
        url = f'{self.api_url}file/{file_id}/'
        return self._request('get', url)

    def put_file(self, file_id: str, serializer_data: Dict):
        url = f'{self.api_url}file/{file_id}/'
        return self._request('put', url, files={'file': serializer_data.get('file')})

    def patch_file(self, file_id: str, serializer_data: Dict):
        url = f'{self.api_url}file/{file_id}/'
        return self._request('patch', url, files={'file': serializer_data.get('file')})

    def delete_file(self, file_id: str):
        url = f'{self.api_url}file/{file_id}/'
        return self._request('delete', url)

    def file_delete_batch(self, serializer_data: Dict):  # TODO пока решили отложить
        url = f'{self.api_url}file/delete-batch/'
        return self._request('post', url)
