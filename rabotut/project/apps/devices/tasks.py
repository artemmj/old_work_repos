from typing import Dict, List

from apps import app
from apps.devices.services import SendPushService


@app.task
def send_push(user_ids: List[str], title: str, message: str, additional_data: Dict):
    """Селери таска отправки пуш уведомлений."""
    SendPushService(user_ids, title, message, additional_data).process()
