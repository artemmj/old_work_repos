import logging
from typing import Dict

from fcm_django.models import FCMDevice
from firebase_admin.exceptions import FirebaseError
from firebase_admin.messaging import Message, Notification

import settings
from apps.helpers.services import AbstractService

logger = logging.getLogger()


class SendPushService(AbstractService):
    """Сервис отправки пуш уведомлений."""

    PUSH_TITLE = 'BT инспектор'
    SITE_URL = settings.SITE_URL

    def __init__(self, user_id: str, message: str, data: Dict):  # noqa: D107
        self.user_id = user_id
        self.message = message
        self.data = data

    def process(self):
        devices = FCMDevice.objects.filter(user_id=self.user_id)
        try:
            devices.send_message(self._gen_message())
        except FirebaseError as e:
            logger.info(str(e))

    def _gen_message(self):
        return Message(
            notification=Notification(
                title=self.PUSH_TITLE,
                body=self.message,
                image=f'{self.SITE_URL}/assets/push_icon.jpeg',
            ),
            data=self.data,
        )
