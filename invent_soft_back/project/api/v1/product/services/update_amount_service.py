from decimal import Decimal

from apps.document.models import Document, DocumentColorChoices, DocumentStatusChoices
from apps.event.models import Event, TitleChoices
from apps.helpers.services import AbstractService
from apps.product.models import ScannedProduct
from apps.task.models import TaskStatusChoices
from apps.zone.models import ZoneStatusChoices


class AmountUpdateService(AbstractService):
    """Сервис обновляет значение amount для ScannedProduct в документе."""

    def __init__(self, scan_product: ScannedProduct, serializer_data: dict):
        self.scan_prd = scan_product
        self.new_amount = Decimal(serializer_data['amount']) if 'amount' in serializer_data else None

    def process(self, *args, **kwargs):
        if not self.new_amount:
            return self.scan_prd

        task = self.scan_prd.task
        task.result -= self.scan_prd.amount
        self.scan_prd.amount = self.new_amount
        self.scan_prd.save()
        task.result += self.new_amount
        task.status = TaskStatusChoices.SUCCESS_SCAN
        task.save()

        document = Document.objects.get(counter_scan_task=task)
        Document.objects.filter(zone=document.zone).exclude(pk=document.pk).update(
            status=DocumentStatusChoices.NOT_READY,
            color=DocumentColorChoices.RED,
        )
        document.status = DocumentStatusChoices.READY
        document.color = DocumentColorChoices.GREEN
        document.save()
        document.zone.status = ZoneStatusChoices.READY
        document.zone.save()

        Event.objects.create(
            project=self.scan_prd.task.zone.project,
            title=TitleChoices.DOCUMENT_SPECIFICATION_EDITING,
            comment=(
                f'Произведена замена спецификации документа; зона: {self.scan_prd.task.zone}, '
                f'изменено количество товара {self.scan_prd.product.title} на {self.new_amount}'  # noqa: WPS326
            ),
        )

        return self.scan_prd
