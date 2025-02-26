from typing import Union

from apps.document.models import Inn, Passport, Registration, Selfie, Snils
from apps.document.models.status.choices import BaseUserDocumentStatuses
from apps.helpers.services import AbstractService


class AcceptDocumentService(AbstractService):
    """Сервис для принятия документа."""

    def __init__(self, document: Union[Inn | Passport | Registration | Selfie | Snils]) -> None:
        self.document = document

    def process(self) -> None:
        self.document.status = BaseUserDocumentStatuses.ACCEPT
        self.document.save()
