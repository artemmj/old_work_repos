from typing import Dict

from django.db.models.query import QuerySet

from apps.document.models import Document
from apps.helpers.services import AbstractService
from apps.task.models import Task, TaskStatusChoices

from .add_scanned_products import AddScanProdsToTaskService


class ProcessAuditorService(AbstractService):
    """Сервис для обработки задания АУДИТОР."""

    def __init__(self, src_task: Dict, db_task: Task, zone_docs: QuerySet):
        self.src_task = src_task
        self.db_task = db_task
        self.zone_docs = zone_docs

    def process(self):
        if Document.objects.filter(zone=self.db_task.zone, auditor_task=self.db_task):
            return

        AddScanProdsToTaskService(self.db_task, self.src_task.get('scanned_products', [])).process()
        self.db_task.status = TaskStatusChoices.WORKED
        self.db_task.save()
        for zone_doc in self.zone_docs:
            zone_doc.auditor_task = self.db_task
            zone_doc.save()
        self.db_task.zone.save()  # для отправки сигнала сокета
