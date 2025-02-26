from typing import Dict, List

from apps.document.models import Document
from apps.helpers.services import AbstractService


class BulkCreateDocumentsService(AbstractService):
    """Сервис массового создания документов."""

    def __init__(self, documents_content: List[Dict]):
        self.documents_content = documents_content

    def process(self):
        Document.objects.bulk_create(
            [
                Document(
                    **document_content,
                )
                for document_content in self.documents_content
            ],
            ignore_conflicts=True,
        )
