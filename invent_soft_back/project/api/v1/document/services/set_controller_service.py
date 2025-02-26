from apps.document.models import Document, DocumentColorChoices, DocumentStatusChoices
from apps.helpers.services import AbstractService
from apps.task.models import Task, TaskStatusChoices
from apps.zone.models import ZoneStatusChoices


class SetDocumentControllerService(AbstractService):
    def __init__(self, document, serializer_data):
        self.document = document
        self.zone = self.document.zone
        self.task = Task.objects.get(pk=serializer_data.get('task'))

    def process(self):
        match = False

        for zdoc in Document.objects.filter(zone=self.zone):
            zdoc.controller_task = self.task

            if zdoc.counter_scan_task.result == zdoc.controller_task.result:
                zdoc.color = DocumentColorChoices.GREEN
                zdoc.status = DocumentStatusChoices.READY
                zdoc.counter_scan_task.status = TaskStatusChoices.SUCCESS_SCAN
                zdoc.controller_task.status = TaskStatusChoices.SUCCESS_SCAN
                match = True
            else:
                zdoc.color = DocumentColorChoices.RED
                zdoc.status = DocumentStatusChoices.NOT_READY
                zdoc.counter_scan_task.status = TaskStatusChoices.FAILED_SCAN
                zdoc.controller_task.status = TaskStatusChoices.FAILED_SCAN

            zdoc.save()
            zdoc.counter_scan_task.save()
            zdoc.controller_task.save()

        self.zone.status = ZoneStatusChoices.READY if match else ZoneStatusChoices.NOT_READY
        self.zone.save()

        return self.document
