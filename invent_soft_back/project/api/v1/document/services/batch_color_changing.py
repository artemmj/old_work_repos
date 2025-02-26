from typing import List

from apps.document.models import Document
from apps.helpers.services import AbstractService
from apps.websocket.services import SendWebSocketInfo


class BatchColorChangingService(AbstractService):
    """Сервис для пакетного изменения цвета у документов."""

    def __init__(self, documents: List[Document], color: str):
        self.documents = documents
        self.color = color

    def process(self, *args, **kwargs):
        for document in self.documents:
            document.prev_color = document.color
            document.color = self.color
            document.color_changed = True

        Document.objects.bulk_update(self.documents, ['prev_color', 'color', 'color_changed'])
        SendWebSocketInfo().send_about_update_documents(documents=self.documents)
        return self.documents
