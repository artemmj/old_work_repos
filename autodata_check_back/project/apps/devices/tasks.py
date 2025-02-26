from typing import Dict

from apps import app
from apps.devices.services import SendPushService


@app.task
def send_push(user_id: str, message: str, data: Dict):
    SendPushService(user_id, message, data)
