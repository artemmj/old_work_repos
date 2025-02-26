from typing import List

from apps.document.models import Document, DocumentColorChoices, DocumentStatusChoices
from apps.helpers.services import AbstractService
from apps.websocket.services import SendWebSocketInfo


class BatchResetColorService(AbstractService):
    """Сервис для пакетного сброса цвета у документов."""

    def __init__(self, documents: List[Document]):
        self.documents = documents

    def process(self, *args, **kwargs):
        for document in self.documents:
            if document.prev_color is None:
                continue

            if document.status == DocumentStatusChoices.READY:
                document.color = DocumentColorChoices.GREEN
            if document.status == DocumentStatusChoices.NOT_READY:
                document.color = DocumentColorChoices.RED

            document.prev_color = None
            document.color_changed = False

        Document.objects.bulk_update(self.documents, ['prev_color', 'color', 'color_changed'])
        SendWebSocketInfo().send_about_update_documents(self.documents)
        return self.documents
