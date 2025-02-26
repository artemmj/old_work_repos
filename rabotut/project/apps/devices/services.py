import logging
from typing import Dict, List

from fcm_django.models import FCMDevice
from firebase_admin.exceptions import FirebaseError
from firebase_admin.messaging import Message, Notification

from apps.helpers.services import AbstractService

logger = logging.getLogger()


class SendPushService(AbstractService):
    """Сервис отправки пуш уведомлений."""

    def __init__(self, user_ids: List[str], title: str, message: str, additional_data: Dict):
        """
        :Args:
            :param user_ids: список id юзеров
            :param title: заголовок пуша
            :param message: текст пуша
            :param additional_data: дополнительные настройки
        """
        self.user_ids = user_ids
        self.title = title
        self.message = message
        self.additional_data = additional_data

    def process(self):
        devices = FCMDevice.objects.filter(user_id__in=self.user_ids, active=True)
        try:
            devices.send_message(self._prepare_message())
        except FirebaseError as e:
            logger.info(f'Ошибка отправки пуша: {str(e)}')

    def _prepare_message(self) -> Message:
        """Подготовка сообщения."""
        return Message(
            notification=Notification(
                title=self.title,
                body=self.message,
            ),
            data=self.additional_data,
        )
