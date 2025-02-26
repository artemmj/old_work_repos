import logging
from typing import Dict, List, Tuple, Union

from django.db.models import QuerySet

from api.v1.document.services.change_document_status_to_ready import ChangeDocumentStatusToReady
from apps.document.models import Document, DocumentColorChoices, DocumentStatusChoices
from apps.employee.models import Employee, EmployeeRoleChoices
from apps.employee.services import LeastLoadedEmployeeService
from apps.helpers.services import AbstractService
from apps.project.models.project import Project
from apps.project.models.terminal_settings_choices import IssuingTaskChoices, RecalculationDiscrepancyChoices
from apps.task.models import Task, TaskStatusChoices, TaskTypeChoices
from apps.terminal.models import Terminal
from apps.zone.models import Zone, ZoneStatusChoices
from apps.zone.services.issuing_tasks import IssuingTasksService

from .add_scanned_products import AddScanProdsToTaskService
from .create_document import CreateDocumentService

logger = logging.getLogger('django')


class ProcessCounterScanService(AbstractService):
    """Сервис для обработки задания СЧЕТЧИК."""

    def __init__(self, src_task: Dict, db_task: Task, zone_docs: QuerySet, terminal: Terminal):
        self.src_task = src_task
        self.db_task = db_task
        self.zone_docs = zone_docs
        self.terminal = terminal
        self.zone = db_task.zone

    def process(self, *args, **kwargs):  # noqa: WPS213
        project = self.db_task.zone.project
        employee = self.db_task.employee

        # Только один документ для СКАН, но есть но
        if Document.objects.filter(zone=self.zone, counter_scan_task=self.db_task):
            return

        AddScanProdsToTaskService(db_task=self.db_task, scan_prods=self.src_task.get('scanned_products', [])).process()
        new_doc = CreateDocumentService(self.src_task, self.db_task, employee, terminal=self.terminal).process()
        self.db_task.status = TaskStatusChoices.WORKED
        self.db_task.save(update_fields=['status'])

        if project.accounting_without_yk:
            self._make_zone_doc_ready(new_doc)

        # self._make_kostyl(employee)  # TODO

        # Если в зоне есть отработанный УК, и если текущий СКАН совпал с каким-то УК - считать Зону готовой.
        # Необходимо пройти по всем УК в зоне и сравнить с каждым, чтобы прописался актуальный, последний.
        z_controller_worked_tasks = Task.objects.filter(
            zone=self.zone,
            type=TaskTypeChoices.CONTROLLER,
        ).exclude(
            status=TaskStatusChoices.INITIALIZED,
        ).order_by('created_at')

        match, success_controller_task = self._check_success_or_fail_scan(z_controller_worked_tasks, new_doc)

        # Так же если сошлось проставить всем документам в зоне, если они есть, этот найденный правильный УК
        if match and self.zone_docs and success_controller_task:
            for zone_doc in self.zone_docs:
                zone_doc.controller_task = success_controller_task
                zone_doc.save(update_fields=['controller_task'])

        # Если не совпал ни с каким УК и если в зоне есть отработанные задания УК - выдать соответственно настройке
        new_tasks = []
        if z_controller_worked_tasks and not match:
            self.db_task.status = TaskStatusChoices.FAILED_SCAN
            self.db_task.save(update_fields=['status'])
            new_tasks = self._assign_tasks_if_fail(project, z_controller_worked_tasks.last().employee)

        self._check_auditors_tasks_for_new_doc(new_doc)

        # Очистить неактуальные задания скан
        del_tasks = Task.objects.filter(
            zone=self.zone, type=TaskTypeChoices.COUNTER_SCAN, status=TaskStatusChoices.INITIALIZED,
        ).exclude(pk__in=new_tasks)
        if del_tasks:
            del_tasks.delete()
        self.zone.save()

    def _make_zone_doc_ready(self, new_doc: Document, z_controllr_task: Union[None, Task] = None):
        """
        Функция переводит задание, зону и документ в статус готовых, для успешной работы.
        Если передается функция последним параметром, проставить ее в документ в УК.
        """
        self.db_task.status = TaskStatusChoices.SUCCESS_SCAN
        self.db_task.save(update_fields=['status'])

        ChangeDocumentStatusToReady(document=new_doc).process()

        if z_controllr_task:
            new_doc.controller_task = z_controllr_task
            new_doc.save(update_fields=['controller_task'])
            z_controllr_task.status = TaskStatusChoices.SUCCESS_SCAN
            z_controllr_task.save(update_fields=['status'])

    def _check_success_or_fail_scan(self, z_controller_worked_tasks, new_doc: Document) -> Tuple[bool, Task]:
        """Функция проверяет, что текущий скан сошелся с каким-то ук. Возвращает кортеж флаг и удачная таска ук."""
        match = False  # флаг совпадения с каким-то ук, успешный скан
        success_controller_task = None  # переменная для хранения задания ук, который сошелся, если такой нашелся

        if z_controller_worked_tasks:
            # На случай, если скан не совпадет ни с каким ук, проставить последний в документ
            new_doc.controller_task = z_controller_worked_tasks.last()
            new_doc.save(update_fields=['controller_task'])
            for z_controllr_task in z_controller_worked_tasks:
                if self.db_task.result == z_controllr_task.result:
                    self._make_zone_doc_ready(new_doc, z_controllr_task=z_controllr_task)
                    match = True
                    success_controller_task = z_controllr_task

        return match, success_controller_task

    def _assign_tasks_if_fail(self, project: Project, employee: Employee) -> Union[List, List[str]]:
        """
        Функция проверяет, что включены настройки для выдачи заданий.
        Если так, решает с какой ролью выдать задания и сколько максимум раз.
        """
        setting_auto = project.rmm_settings.auto_zones_amount
        setting_recalc = project.terminal_settings.recalculation_discrepancy

        new_tasks = []
        if setting_recalc == RecalculationDiscrepancyChoices.SCAN:
            if setting_auto > 0:
                # Если вкл настройки кол-во автоназначаемых зон и выдачи задания на
                # СКАН - выдать не более 3 раз, если настройка на УК - выдать в любом случае
                zone_cs_tasks = Task.objects.filter(zone=self.zone, type=TaskTypeChoices.COUNTER_SCAN)
                if zone_cs_tasks.count() < 3:
                    new_tasks = IssuingTasksService(
                        zone=self.zone, employees=[self.db_task.employee], role=TaskTypeChoices.COUNTER_SCAN,
                    ).process()
            else:
                new_tasks = IssuingTasksService(
                    zone=self.zone, employees=[self.db_task.employee], role=TaskTypeChoices.COUNTER_SCAN,
                ).process()
        elif setting_recalc == RecalculationDiscrepancyChoices.CONTROLLER:
            new_tasks = IssuingTasksService(
                zone=self.zone, employees=[employee], role=TaskTypeChoices.CONTROLLER,
            ).process()
        return new_tasks

    def _check_auditors_tasks_for_new_doc(self, new_doc: Document):
        """Нужно присвоить документу последние актуальные задания аудиторов, если есть"""
        auditor_zone_tasks = Task.objects.filter(zone=self.zone, type=TaskTypeChoices.AUDITOR)
        auditor_zone_tasks = auditor_zone_tasks.exclude(status=TaskStatusChoices.INITIALIZED).order_by('created_at')
        if auditor_zone_tasks:
            new_doc.auditor_task = auditor_zone_tasks.last()
            new_doc.save(update_fields=['auditor_task'])

        auditor_ext_zone_tasks = Task.objects.filter(zone=self.zone, type=TaskTypeChoices.AUDITOR_EXTERNAL)
        auditor_ext_zone_tasks = auditor_ext_zone_tasks.exclude(status=TaskStatusChoices.INITIALIZED)
        if auditor_ext_zone_tasks:
            new_doc.auditor_external_task = auditor_ext_zone_tasks.order_by('created_at').last()
            new_doc.save(update_fields=['auditor_external_task'])

        auditor_contr_zone_tasks = Task.objects.filter(zone=self.zone, type=TaskTypeChoices.AUDITOR_CONTROLLER)
        auditor_contr_zone_tasks = auditor_contr_zone_tasks.exclude(status=TaskStatusChoices.INITIALIZED)
        if auditor_contr_zone_tasks:
            new_doc.auditor_controller_task = auditor_contr_zone_tasks.order_by('created_at').last()
            new_doc.save(update_fields=['auditor_controller_task'])

    def _make_kostyl(self, db_employee):
        """
        Костыль. При ситуации, когда работает два человека с двух терминалов под счетчиком
        под одним пользователем в одной таске. Необходимо создать таску под второго пользователя,
        если зона и таска совпадают, создать документ под второго человека. Выдать задание УК.
        """
        last_doc = self.zone_docs.last()
        project = self.db_task.zone.project

        if (  # noqa: WPS337
            last_doc
            and self.zone_docs.count() == 1
            and last_doc.terminal != self.terminal
            and last_doc.counter_scan_task == self.db_task
        ):
            newtask = Task.objects.create(
                zone=self.db_task.zone,
                employee=db_employee,
                type=TaskTypeChoices.COUNTER_SCAN,
                status=TaskStatusChoices.WORKED,
                terminal=self.terminal,
            )
            AddScanProdsToTaskService(newtask, self.src_task.get('scanned_products', [])).process()
            doc = CreateDocumentService(
                self.src_task,
                self.db_task.zone,
                db_employee,
                terminal=self.terminal,
            ).process()
            employee = None
            if project.terminal_settings.issuing_task == IssuingTaskChoices.CURRENT_USER:
                employee = Employee.objects.get(pk=self.src_task['document']['employee'])
            elif project.terminal_settings.issuing_task == IssuingTaskChoices.LEAST_LOADED_USER:
                employee = LeastLoadedEmployeeService(
                    project=project,
                    role=EmployeeRoleChoices.COUNTER,
                    task_type=TaskTypeChoices.CONTROLLER,
                    exclude_ids=[],
                ).process()

            # Создание задания на С.УК при соблюдении условий автоназначения
            if employee and project.auto_assign_enbale and project.rmm_settings.auto_zones_amount > 0:
                cctask = Task.objects.create(
                    zone=self.db_task.zone,
                    employee=employee,
                    type=TaskTypeChoices.CONTROLLER,
                )
                doc.counter_controller_task = cctask
                doc.save()
