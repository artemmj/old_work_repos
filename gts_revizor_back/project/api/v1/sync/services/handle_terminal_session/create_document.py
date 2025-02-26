from typing import Dict

from apps.document.models import Document, DocumentColorChoices
from apps.employee.models import Employee
from apps.helpers.services import AbstractService
from apps.task.models import Task, TaskTypeChoices
from apps.terminal.models import Terminal


class CreateDocumentService(AbstractService):
    """Сервис для создания документа."""

    def __init__(self, src_task: Dict, db_task: Task, db_employee: Employee, terminal: Terminal):
        self.src_task = src_task
        self.db_task = db_task
        self.db_employee = db_employee
        self.terminal = terminal

    def process(self) -> Document:
        """Создать документ, использовать только по назначению, только для счетчика."""
        zone_docs = Document.objects.filter(zone=self.db_task.zone).order_by('created_at')
        # Для второго документа в зоне цвет красный, для 3-го и последующих - фиолетовый
        color = DocumentColorChoices.RED if zone_docs.count() < 2 else DocumentColorChoices.VIOLET

        # Проверить, в зависимости от настройки терминала Подозрительное кол-во для ШК, является ли
        # документ подозрительным - если каких-то товаров больше чем значение настройки
        suspicious = False
        for prd in self.db_task.scanned_products.all():
            if prd.amount > self.db_task.zone.project.terminal_settings.suspicious_barcodes_amount:  # noqa: WPS219
                suspicious = True

        return Document.objects.create(
            zone=self.db_task.zone,
            employee=self.db_employee,
            start_audit_date=self.src_task.get('document').get('start_audit_date'),
            end_audit_date=self.src_task.get('document').get('end_audit_date'),
            tsd_number=self.src_task.get('document').get('tsd_number'),
            suspicious=suspicious,
            color=color,
            terminal=self.terminal,
            counter_scan_task=self.db_task,
        )
