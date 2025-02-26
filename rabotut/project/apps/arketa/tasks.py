from typing import Dict

from apps import app
from apps.arketa.clients import ArketaServiceApiClient
from apps.document.models.status.choices import BaseUserDocumentStatuses
from apps.user.models import User

from .services.send_doc_service import SendDocumentToArketaService


@app.task
def create_user_in_arketa():
    """Создание пользователя в Аркете."""
    users = User.objects.prefetch_related('inn', 'passport').filter(
        arketa_user_id__isnull=True,
        passport__isnull=False,
        passport__status=BaseUserDocumentStatuses.ACCEPT,
        inn__isnull=False,
        inn__status=BaseUserDocumentStatuses.ACCEPT,
    )
    for user in users:
        arketa_user_data = ArketaServiceApiClient().create_user(user)
        user.arketa_user_id = arketa_user_data.get('id')
        user.save()


@app.task
def change_user_phone_in_arketa(user_id: str, phone: str):
    """Изменение номера телефона пользователя в аркете."""
    ArketaServiceApiClient().change_user_phone(user_id=user_id, phone=phone)


@app.task
def send_document_to_arketa_task(model: str, user_id: str, document_data: Dict):
    """Таска для отправки документа в аркету - нового, либо обновленного."""
    return SendDocumentToArketaService(model=model, user_id=user_id, document_data=document_data).process()
