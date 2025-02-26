from typing import Union

from apps.document.models import Inn, Passport, Registration, Selfie, Snils
from apps.document.models.status.choices import BaseUserDocumentStatuses
from apps.helpers.services import AbstractService
from apps.user.models.doc_statuses import UserDocStatuses

DOCUMENT_MODELS = [Inn, Passport, Registration, Selfie, Snils]


class CalculateUserStatusService(AbstractService):
    """Рассчитывает статус подработчика на основе статусов его обязательных документов."""

    def __init__(self, document: Union[Inn, Passport, Registration, Selfie, Snils]):
        self.document = document

    def process(self):
        statuses = {self.get_doc_status(model) for model in DOCUMENT_MODELS}
        doc_status = UserDocStatuses.APPROVAL
        match statuses:
            case _ if BaseUserDocumentStatuses.DECLINE in statuses:
                doc_status = UserDocStatuses.DECLINE
            case _ if statuses == {BaseUserDocumentStatuses.ACCEPT}:
                doc_status = UserDocStatuses.ACCEPT
        self.document.user.doc_status = doc_status
        self.document.user.save()

    def get_doc_status(self, model) -> str:
        document = model.objects.filter(user=self.document.user).first()
        return document.status if document else BaseUserDocumentStatuses.APPROVAL
