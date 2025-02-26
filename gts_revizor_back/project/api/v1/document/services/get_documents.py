from typing import Dict

from apps.document.models import Document
from apps.helpers.services import AbstractService


class GetDocumentsService(AbstractService):
    """Сервис получения списка документов."""

    def __init__(self, filter_params: Dict[str, str] = None):
        self.filter_params = filter_params

    def process(self):
        documents = (
            Document
            .objects
            .select_related(
                'employee',
                'zone',
                'counter_scan_task',
                'controller_task',
            )
            .with_counter_scan_barcode_amount()
            .with_controller_barcode_amount()
            .with_auditor_barcode_amount()
            .with_auditor_controller_barcode_amount()
            .with_color_numbers()
            .order_by('fake_id')
        )

        return documents.filter(**self.filter_params) if self.filter_params else documents
