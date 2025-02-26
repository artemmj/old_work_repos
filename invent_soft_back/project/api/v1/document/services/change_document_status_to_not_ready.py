from django.db import transaction

from apps.document.models import Document, DocumentColorChoices, DocumentStatusChoices
from apps.helpers.services import AbstractService
from apps.zone.models import ZoneStatusChoices


class ChangeDocumentStatusToNotReady(AbstractService):
    """Сервис для изменения статуса документа на Не готов."""

    def __init__(self, document: Document):
        self.document = document

    def process(self, *args, **kwargs):
        with transaction.atomic():
            document = self.document
            zone = document.zone

            document.status = DocumentStatusChoices.NOT_READY
            document.color = DocumentColorChoices.RED
            zone.status = ZoneStatusChoices.NOT_READY

            zone.save()
            document.save()
