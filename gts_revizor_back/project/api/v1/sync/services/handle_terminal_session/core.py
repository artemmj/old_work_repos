import logging
from typing import Dict, List

from api.v1.task.serializers import TaskReadSerializer
from apps.document.models import Document
from apps.helpers.services import AbstractService
from apps.task.models import Task, TaskTypeChoices
from apps.terminal.models import Terminal
from apps.zone.models import Zone, ZoneStatusChoices

from .check_auto_assign import CheckAutoAssignService
from .check_create_controller_task import CheckCreateControllerTaskService
from .process_auditor import ProcessAuditorService
from .process_auditor_controller import ProcessAuditorControllerService
from .process_auditor_external import ProcessAuditorExternalService
from .process_controller import ProcessControllerService
from .process_counter_scan import ProcessCounterScanService

logger = logging.getLogger('django')


class HandleTerminalSessionService(AbstractService):
    """Сервис обрабатывает запрос терминала с данными о сессии работы."""

    def __init__(self, serializer_data: Dict):
        self.serializer_data = serializer_data

    def process(self) -> List[Dict]:  # noqa: WPS231
        terminal = Terminal.objects.get(pk=self.serializer_data.get('terminal'))
        # t_time = datetime.strptime(self.serializer_data.get('terminal_time')[:19], '%Y-%m-%dT%H:%M:%S')  # noqa: E800
        processed_tasks = []

        for srcuser in self.serializer_data.get('users'):
            for src_task in srcuser.get('tasks'):
                task = Task.objects.get(pk=src_task['id'])
                task.terminal = terminal
                task.save(update_fields=['terminal'])
                zone = Zone.objects.get(pk=src_task['document']['zone'])

                zone_documents = Document.objects.filter(zone=zone).order_by('created_at')
                func_map = {
                    TaskTypeChoices.COUNTER_SCAN: ProcessCounterScanService(src_task, task, zone_documents, terminal),
                    TaskTypeChoices.CONTROLLER: ProcessControllerService(src_task, task, zone_documents),
                    TaskTypeChoices.AUDITOR: ProcessAuditorService(src_task, task, zone_documents),
                    TaskTypeChoices.AUDITOR_CONTROLLER: ProcessAuditorControllerService(src_task, task, zone_documents),
                    TaskTypeChoices.AUDITOR_EXTERNAL: ProcessAuditorExternalService(src_task, task, zone_documents),
                }
                func_map[task.type].process()

                zone = Zone.objects.get(pk=src_task['document']['zone'])
                if task.type in {TaskTypeChoices.COUNTER_SCAN, TaskTypeChoices.CONTROLLER}:
                    if task.type == TaskTypeChoices.COUNTER_SCAN and zone.status == ZoneStatusChoices.NOT_READY:
                        CheckCreateControllerTaskService(db_zone=zone, db_employee=task.employee).process()
                    CheckAutoAssignService(db_task=task).process()

                processed_tasks.append(TaskReadSerializer(task).data)

        return processed_tasks
