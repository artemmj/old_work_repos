from typing import Union

from apps.document.models import Inn, Passport, Registration, Selfie, Snils
from apps.document.models.status.choices import BaseUserDocumentStatuses
from apps.helpers.services import AbstractService
from apps.user.models import UserRoles


class ApprovalDocumentService(AbstractService):
    """Сервис перевода документа в статус Проверка."""

    def __init__(self, document: Union[Inn | Passport | Registration | Selfie | Snils], user_role: UserRoles):
        self.document = document
        self.user_role = user_role

    def process(self):
        if self.document.status == BaseUserDocumentStatuses.DECLINE and self.user_role != UserRoles.MASTER:
            self.document.status = BaseUserDocumentStatuses.APPROVAL
            self.document.save()
