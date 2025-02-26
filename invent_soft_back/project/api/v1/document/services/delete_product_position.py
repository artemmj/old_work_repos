from apps.document.models import Document, DocumentColorChoices, DocumentStatusChoices
from apps.event.models import Event, TitleChoices
from apps.helpers.services import AbstractService
from apps.product.models import ScannedProduct
from apps.task.models import TaskStatusChoices
from apps.zone.models import ZoneStatusChoices


class DeleteProductPositionService(AbstractService):
    """Сервис для удаления позиции отсканированного товара в документе."""

    def __init__(self, document: Document, serializer_data: dict):
        self.document = document
        self.scanned_product = ScannedProduct.objects.get(pk=serializer_data['product'])

    def process(self, *args, **kwargs):
        product_title = self.scanned_product.product.title

        Document.objects.filter(zone=self.document.zone).exclude(pk=self.document.pk).update(
            status=DocumentStatusChoices.NOT_READY,
            color=DocumentColorChoices.RED,
        )
        self.document.counter_scan_task.result -= self.scanned_product.amount
        self.document.counter_scan_task.status = TaskStatusChoices.SUCCESS_SCAN
        self.document.counter_scan_task.save()
        self.document.zone.status = ZoneStatusChoices.READY
        self.document.zone.save()
        self.scanned_product.delete()
        self.document.status = DocumentStatusChoices.READY
        self.document.color = DocumentColorChoices.GREEN
        self.document.save()

        Event.objects.create(
            project=self.document.zone.project,
            title=TitleChoices.DOCUMENT_SPECIFICATION_EDITING,
            comment=(
                'Произведена замена спецификации документа; зона: '
                f'{self.document.zone}, документ: {self.document.pk}, '  # noqa: WPS326
                f'удалена строка ({product_title})"'  # noqa: WPS326
            ),
        )

        return self.document
