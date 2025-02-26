import logging

from apps.document.models import Document, DocumentColorChoices, DocumentStatusChoices
from apps.event.models import Event, TitleChoices
from apps.helpers.services import AbstractService
from apps.product.models import Product, ScannedProduct
from apps.task.models import TaskStatusChoices
from apps.zone.models import ZoneStatusChoices

logger = logging.getLogger('django')


class AddProductPositionService(AbstractService):
    """Сервис для добавления позиции отсканированного товара в документ."""

    def __init__(self, document: Document, serializer_data: dict):
        self.document = document
        self.barcode = serializer_data['barcode']
        self.amount = serializer_data['amount']

    def process(self, *args, **kwargs):
        product = Product.objects.get(barcode=self.barcode, project=self.document.zone.project)
        scan_product, created = ScannedProduct.objects.get_or_create(
            product=product,
            task=self.document.counter_scan_task,
            defaults={'amount': self.amount},
        )
        if not created:
            scan_product.amount += self.amount
            scan_product.save()

        Document.objects.filter(zone=self.document.zone).exclude(pk=self.document.pk).update(
            status=DocumentStatusChoices.NOT_READY,
            color=DocumentColorChoices.RED,
        )
        self.document.status = DocumentStatusChoices.READY
        self.document.color = DocumentColorChoices.GREEN
        self.document.save()
        self.document.zone.status = ZoneStatusChoices.READY
        self.document.zone.save()
        self.document.counter_scan_task.result += self.amount
        self.document.counter_scan_task.status = TaskStatusChoices.SUCCESS_SCAN
        self.document.counter_scan_task.save()

        Event.objects.create(
            project=self.document.zone.project,
            title=TitleChoices.DOCUMENT_SPECIFICATION_EDITING,
            comment=(
                f'Произведена замена спецификации документа; зона: {self.document.zone}, '
                f'документ: {self.document.pk}, добавлена новая строка ({product.title}, '  # noqa: WPS326
                f'кол-во {self.amount})"'  # noqa: WPS326
            ),
        )

        return self.document
