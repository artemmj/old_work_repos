import logging
from decimal import Decimal
from typing import Dict

from django.db.models import QuerySet

from apps.document.models import Document, DocumentColorChoices, DocumentStatusChoices
from apps.helpers.services import AbstractService
from apps.project.models.terminal_settings_choices import RecalculationDiscrepancyChoices
from apps.task.models import Task, TaskStatusChoices, TaskTypeChoices
from apps.zone.models import ZoneStatusChoices
from apps.zone.services.issuing_tasks import IssuingTasksService

logger = logging.getLogger('django')


class ProcessControllerService(AbstractService):
    """Сервис для обработки задания УК."""

    def __init__(self, src_task: Dict, db_task: Task, zone_docs: QuerySet):
        self.src_task = src_task
        self.db_task = db_task
        self.zone_docs = zone_docs

    def process(self):
        zone = self.db_task.zone
        self.db_task.result = self.src_task.get('result')
        self.db_task.status = TaskStatusChoices.WORKED
        self.db_task.save(update_fields=['status', 'result'])

        # Очистить неактуальные задания УК
        Task.objects.filter(zone=zone, type=TaskTypeChoices.CONTROLLER, status=TaskStatusChoices.INITIALIZED).delete()
        zone.save()

        # Если в зоне нет документов - все сделано, выходим
        if not self.zone_docs:
            return

        match = self._check_documents_match()
        # Если не сошлись, в зависимости от настройки recalculation_discrepancy выдать новое задание + есть условия
        if not match:
            self._assign_if_fail()
        zone.save()

    def _check_documents_match(self) -> bool:
        """Фукнция проверяет все документы в зоне и пытается найти совпадение."""
        match = False
        zone = self.db_task.zone
        success_document = None

        for zone_doc in self.zone_docs:
            # Каждому документу в зоне проставить текущую таску ук
            zone_doc.controller_task = self.db_task
            zone_doc.save(update_fields=['controller_task'])

            if zone_doc.counter_scan_task.result == round(Decimal(self.db_task.result), 3):
                match = True
                self.db_task.status = TaskStatusChoices.SUCCESS_SCAN
                zone.status = ZoneStatusChoices.READY
                zone.save(update_fields=['status'])
                zone_doc.status = DocumentStatusChoices.READY
                zone_doc.color = DocumentColorChoices.GREEN
                zone_doc.save(update_fields=['status', 'color'])
                zone_doc.counter_scan_task.status = TaskStatusChoices.SUCCESS_SCAN
                zone_doc.counter_scan_task.save(update_fields=['status'])
                success_document = zone_doc
            else:
                self.db_task.status = TaskStatusChoices.FAILED_SCAN
            self.db_task.save(update_fields=['status'])

        if match:
            # Удалить назначенные задания СКАН если совпало
            Task.objects.filter(
                zone=zone,
                type=TaskTypeChoices.COUNTER_SCAN,
                status=TaskStatusChoices.INITIALIZED,
            ).delete()

            ready_documents = Document.objects.filter(
                zone=zone,
                status=DocumentStatusChoices.READY,
            ).exclude(
                pk=success_document.pk,
            )

            # Для отработки @hook(AFTER_UPDATE) https://git.your-site.pro/gts_revizor/gts_revizor_back/-/issues/435
            for ready_document in ready_documents:
                ready_document.color = DocumentColorChoices.RED
                ready_document.status = DocumentStatusChoices.NOT_READY
                ready_document.save()

        return match

    def _assign_if_fail(self):
        """
        Функция, в случае если не было никакого совпадения с документами,
        в зависимости от настроет проекта выдает новое задание.
        """
        zone = self.db_task.zone
        project = zone.project
        self.db_task.status = TaskStatusChoices.FAILED_SCAN
        self.db_task.save(update_fields=['status'])

        worked_statuses = (TaskStatusChoices.WORKED, TaskStatusChoices.SUCCESS_SCAN, TaskStatusChoices.FAILED_SCAN)
        zone_counter_scan_tasks = Task.objects.filter(
            zone=zone, type=TaskTypeChoices.COUNTER_SCAN, status__in=worked_statuses,
        )
        zone_counter_scan_tasks.update(status=TaskStatusChoices.FAILED_SCAN)

        setting_recals = project.terminal_settings.recalculation_discrepancy
        if setting_recals == RecalculationDiscrepancyChoices.SCAN:
            # Выбрана настройка СКАН - выдать на скан на сотр. из последнего документа
            if zone_counter_scan_tasks:
                employee = zone_counter_scan_tasks.order_by('created_at').last().employee
                IssuingTasksService(zone=zone, employees=[employee], role=TaskTypeChoices.COUNTER_SCAN).process()
        elif setting_recals == RecalculationDiscrepancyChoices.CONTROLLER:
            # Выбрана настройка УК - выдать на УК соотв. условиям
            self._work_with_recals_settings_controller(zone_counter_scan_tasks)

    def _work_with_recals_settings_controller(self, zone_counter_scan_tasks: QuerySet):
        """
        Функция если нет заданий ук выдает его, если есть либо выдает скан если результат
        совпадает с существующим, либо выдат ук не более 3 раз, когда 3 - выдать скан, и так по кругу.
        """
        zone = self.db_task.zone
        zone_controller_tasks = Task.objects.filter(zone=zone, type=self.db_task.type)
        if zone_controller_tasks.exclude(pk=self.db_task.pk).count() == 0:
            IssuingTasksService(zone=zone, employees=[self.db_task.employee], role=self.db_task.type).process()
        else:
            # Если в зоне 1 задание УК, и его результат сходится с тем что пришел - выдать на переСКАН
            if (  # noqa: WPS337
                zone_controller_tasks.exclude(pk=self.db_task.pk).count() == 1
                and zone_controller_tasks.exclude(pk=self.db_task.pk).first().result == self.db_task.result
                and zone_counter_scan_tasks
            ):
                employee = zone_counter_scan_tasks.order_by('created_at').last().employee
                IssuingTasksService(zone=zone, employees=[employee], role=TaskTypeChoices.COUNTER_SCAN).process()
            else:
                # Пока заданий УК в зоне меньше чем в 3 раза чем СКАН - выдавать УК
                if zone_controller_tasks.count() / zone_counter_scan_tasks.count() < 3:
                    IssuingTasksService(
                        zone=zone,
                        employees=[self.db_task.employee],
                        role=TaskTypeChoices.CONTROLLER,
                    ).process()
                # когда ровно в 3 - СКАН
                else:
                    employee = zone_counter_scan_tasks.first().employee
                    IssuingTasksService(zone=zone, employees=[employee], role=TaskTypeChoices.COUNTER_SCAN).process()
