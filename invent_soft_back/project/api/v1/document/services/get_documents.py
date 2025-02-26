from apps.document.models import Document
from apps.helpers.services import AbstractService


class GetDocumentsService(AbstractService):
    """Сервис получения списка документов."""

    def process(self):
        return (
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
            .order_by('fake_id')
        )
