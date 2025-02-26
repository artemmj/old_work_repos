from typing import Union

from apps.document.models import Inn, Passport, Registration, Selfie, Snils
from apps.document.models.status.choices import BaseUserDocumentStatuses
from apps.helpers.services import AbstractService


class DeclineDocumentService(AbstractService):
    """Сервис для отклонения документа."""

    def __init__(
        self,
        document: Union[Inn | Passport | Registration | Selfie | Snils],
        rejection_reason: str,
    ) -> None:
        self.document = document
        self.rejection_reason = rejection_reason

    def process(self) -> None:
        self.document.status = BaseUserDocumentStatuses.DECLINE
        if self.rejection_reason:
            self.document.rejection_reason = self.rejection_reason
        self.document.save()
