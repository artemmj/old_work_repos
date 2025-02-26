import json
import logging
from typing import List

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

from apps.websocket.formatters import ErrorFormatter

channel_layer = get_channel_layer()
logger = logging.getLogger('django')


class WebsocketConsumer(AsyncWebsocketConsumer):
    """Класс для обработки websocket соединений"""

    async def connect(self):
        await self.accept()
        if not self.scope.get('user_id'):
            await self.send_error(['Invalid token payload'], 401)
            await self.close()
            return

        self.user_id = self.scope['user_id']
        # Подключение к комнате
        await self.channel_layer.group_add('default_room', self.channel_name)

    async def disconnect(self, close_code):
        # Отключение от комнаты
        await self.channel_layer.group_discard('default_room', self.channel_name)

    async def receive(self, text_data):
        pass  # noqa: WPS420

    async def send_data(self, event):
        # Отправка сообщения обратно на клиент
        await self.send(text_data=json.dumps(event['data']))

    async def send_error(self, errors, code):
        error_data = ErrorFormatter().format(errors, code)
        await self.send(
            json.dumps({'type': 'error', 'data': error_data}),
        )
