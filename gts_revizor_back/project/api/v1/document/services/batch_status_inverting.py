from typing import List

from api.v1.document.services.change_document_status_to_not_ready import ChangeDocumentStatusToNotReady
from api.v1.document.services.change_document_status_to_ready import ChangeDocumentStatusToReady
from apps.document.models import Document, DocumentStatusChoices
from apps.helpers.services import AbstractService


class BatchStatusInvertingService(AbstractService):
    """Сервис для пакетного инвертирования статуса у документов."""

    def __init__(self, documents: List[Document]):
        self.documents = documents

    def process(self, *args, **kwargs):
        for document in self.documents:

            if document.status == DocumentStatusChoices.READY:
                ChangeDocumentStatusToNotReady(document).process()
            elif document.status == DocumentStatusChoices.NOT_READY:
                ChangeDocumentStatusToReady(document).process()

        return self.documents
