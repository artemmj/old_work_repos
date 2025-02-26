from typing import List

from api.v1.document import services as docs_services
from apps.document.models import Document
from apps.helpers.services import AbstractService


class BatchReplaceDocumentSpecificationService(AbstractService):
    """Сервис для пакетной замены спецификации у документов."""

    def __init__(self, document_ids: List[int], source: str):
        self.document_ids = document_ids
        self.source = source

    def process(self, *args, **kwargs):
        documents = Document.objects.filter(pk__in=self.document_ids)

        for document in documents:
            docs_services.ReplaceDocumentSpecificationService().process(self.source, document)

        return documents
