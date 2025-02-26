from typing import List

from apps.document.models import Document
from apps.helpers.services import AbstractService


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
            document.save(update_fields=['prev_color', 'color', 'color_changed'])

        return self.documents
