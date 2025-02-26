from django.db import transaction

from apps.document.models import Document, DocumentColorChoices, DocumentStatusChoices
from apps.helpers.services import AbstractService
from apps.zone.models import ZoneStatusChoices


class ChangeDocumentStatusToReady(AbstractService):
    """Сервис для изменения статуса документа на Готов."""

    def __init__(self, document: Document):
        self.document = document

    def process(self, *args, **kwargs):
        with transaction.atomic():
            document = self.document
            zone = document.zone

            zone.status = ZoneStatusChoices.READY
            (  # noqa: B018 WPS428
                zone
                .documents
                .exclude(id=document.id)
                .exclude(status=DocumentStatusChoices.NOT_READY)
                .update(
                    status=DocumentStatusChoices.NOT_READY,
                    color=DocumentColorChoices.RED,
                ),
            )
            document.status = DocumentStatusChoices.READY
            document.color = DocumentColorChoices.GREEN

            zone.save()
            document.save()
