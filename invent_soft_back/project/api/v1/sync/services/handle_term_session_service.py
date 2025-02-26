import logging
from datetime import datetime
from decimal import Decimal
from typing import Dict, Generator, List

from django.db.models.query import QuerySet

from api.v1.task.serializers import TaskReadSerializer
from apps.document.models import Document, DocumentColorChoices, DocumentStatusChoices
from apps.employee.models import Employee, EmployeeRoleChoices
from apps.employee.services import LeastLoadedEmployeeService
from apps.helpers.services import AbstractService
from apps.product.models import Product, ScannedProduct
from apps.project.models import Project
from apps.project.models.terminal_settings_choices import IssuingTaskChoices, RecalculationDiscrepancyChoices
from apps.task.models import Task, TaskStatusChoices, TaskTypeChoices
from apps.terminal.models import Terminal
from apps.websocket.services import SendWebSocketInfo
from apps.zone.models import Zone, ZoneStatusChoices
from apps.zone.services.issuing_tasks import IssuingTasksService

logger = logging.getLogger('django')


class HandleTerminalSessionService(AbstractService):  # noqa: WPS338 WPS214
    """
    Сервис обрабатывает запрос терминала с данными о сессии работы. Запрос терминала может содержать
        много тасок/пользователей, т.к. например терминал работал оффлайн, пока не было соединения.
    """

    def __init__(self, serializer_data: Dict):
        self.project: Project = Employee.objects.get(pk=serializer_data.get('users')[0]['id']).project
        self.terminal: Terminal = Terminal.objects.get(pk=serializer_data.get('terminal'))
        self.users: List[Dict] = serializer_data.get('users')
        self.terminal_time = datetime.strptime(serializer_data.get('terminal_time')[:19], '%Y-%m-%dT%H:%M:%S')

    def _srctasks_generator(self) -> Generator:
        for srcuser in self.users:
            for srctask in srcuser.get('tasks'):  # noqa: WPS526
                yield srcuser, srctask

    def process(self) -> List[Dict]:  # noqa: WPS231 WPS213
        processed_tasks = []
        for srcuser, srctask in self._srctasks_generator():
            db_task = Task.objects.get(pk=srctask['id'])
            db_zone = Zone.objects.get(pk=srctask['document']['zone'])
            db_employee = Employee.objects.get(pk=srcuser['id'])

            db_task.terminal = self.terminal
            db_task.employee = db_employee
            db_task.save()

            zone_docs = Document.objects.filter(zone=db_zone).order_by('created_at')
            if db_task.type == TaskTypeChoices.COUNTER_SCAN:  # noqa: WPS223
                self._process_counter_scan(srctask, db_task, db_employee, zone_docs)
            elif db_task.type == TaskTypeChoices.CONTROLLER:
                self._process_controller(srctask, db_zone, db_task)
            elif db_task.type == TaskTypeChoices.AUDITOR:
                self._process_auditor(srctask, db_task, zone_docs)
            elif db_task.type == TaskTypeChoices.AUDITOR_CONTROLLER:
                self._process_auditor_controller(srctask, db_task, zone_docs)
            elif db_task.type == TaskTypeChoices.AUDITOR_EXTERNAL:
                self._process_auditor_ext(srctask, db_task, zone_docs)

            if db_task.type in (TaskTypeChoices.COUNTER_SCAN, TaskTypeChoices.CONTROLLER):  # noqa: WPS510
                if db_task.type == TaskTypeChoices.COUNTER_SCAN:
                    self._create_controller_task(db_zone=db_zone, db_employee=db_employee)
                self._check_autoassign(db_employee=db_employee, db_task=db_task)

            processed_tasks.append(TaskReadSerializer(db_task).data)
            SendWebSocketInfo().send_about_update_zones(zones=[db_zone])

        return processed_tasks

    def _add_scanprods_to_task(self, db_task: Task, scan_prods: List) -> None:
        """Добавить отсканированные товары в таску."""
        for scanned in scan_prods:
            # Пытаемся найти товар по полному совпадению, либо ставим как неизвестный
            barcode = scanned['product']
            if scanned.get('is_weight_product', False):
                barcode = scanned['product'][:7]

            attempt_products = Product.objects.filter(
                project=self.project,
                title=scanned.get('title', None),
                barcode=barcode,
                vendor_code=scanned.get('vendor_code', None),
            )

            if attempt_products:
                db_product = attempt_products.first()
            else:
                db_product, _ = Product.objects.get_or_create(
                    project=self.project,
                    barcode=scanned['product'],
                    vendor_code=f'art_{scanned["product"]}',
                    title='Неизвестный товар',
                )

            amount = scanned.get('amount')
            if scanned.get('is_weight_product', False):  # весовой товар, в килограммы
                amount = Decimal(amount / 1000)

            scan_prd_create_data = {
                'product': db_product,
                'task': db_task,
                'defaults': {
                    'amount': amount,
                    'added_by_product_code': scanned.get('added_by_product_code'),
                    'is_weight': scanned.get('is_weight_product'),
                    'scanned_time': scanned.get('scanned_time'),
                },
            }
            if scanned.get('dm', None):
                scan_prd_create_data['dm'] = scanned.get('dm')
            newscanned, created = ScannedProduct.objects.get_or_create(**scan_prd_create_data)
            if not created:
                newscanned.amount += amount
                newscanned.save()
            db_task.result += amount

        db_task.result = round(db_task.result, 3)
        db_task.save()

    def _create_document(self, task: Dict, db_task: Task, db_zone: Zone, db_employee: Employee) -> Document:
        """Создать документ, использовать только по назначению, для СКАН."""
        zone_docs = Document.objects.filter(zone=db_zone).order_by('created_at')
        # Для второго документа в зоне цвет красный, для 3-го и последующих - фиолетовый
        color = DocumentColorChoices.RED if zone_docs.count() < 2 else DocumentColorChoices.VIOLET

        # Проверить, в зависимости от настройки терминала Подозрительное кол-во для ШК, является ли
        # документ подозрительным - если каких-то товаров больше чем значение настройки
        suspicious = False
        for prd in db_task.scanned_products.all():
            if prd.amount > db_task.zone.project.terminal_settings.suspicious_barcodes_amount:
                suspicious = True

        new_document = Document.objects.create(
            zone=db_zone,
            employee=db_employee,
            start_audit_date=task.get('document').get('start_audit_date'),
            end_audit_date=task.get('document').get('end_audit_date'),
            tsd_number=task.get('document').get('tsd_number'),
            suspicious=suspicious,
            color=color,
            terminal=self.terminal,
            counter_scan_task=db_task if db_task.type == TaskTypeChoices.COUNTER_SCAN else None,
            auditor_task=db_task if db_task.type == TaskTypeChoices.AUDITOR else None,
            auditor_controller_task=db_task if db_task.type == TaskTypeChoices.AUDITOR_CONTROLLER else None,
            auditor_external_task=db_task if db_task.type == TaskTypeChoices.AUDITOR_EXTERNAL else None,
        )
        SendWebSocketInfo().send_about_new_documents(documents=[new_document])
        return new_document

    def _process_counter_scan(  # noqa: WPS231 WPS213
        self,
        srctask: Dict,
        db_task: Task,
        db_employee: Employee,
        zone_docs: QuerySet,
    ):
        """Обработка задания СЧЕТЧИК."""
        if Document.objects.filter(zone=db_task.zone, counter_scan_task=db_task):
            # Только один документ для СКАН
            return
        self._add_scanprods_to_task(db_task, srctask.get('scanned_products', []))
        newdocument = self._create_document(srctask, db_task, db_task.zone, db_employee)
        db_task.status = TaskStatusChoices.WORKED
        db_task.save()

        need_send_signal = False

        # Если настройка вкл., сразу после СКАН документ готов и зеленый
        if self.project.accounting_without_yk:
            newdocument.status = DocumentStatusChoices.READY
            newdocument.color = DocumentColorChoices.GREEN
            newdocument.save()
            db_task.zone.status = ZoneStatusChoices.READY
            db_task.status = TaskStatusChoices.SUCCESS_SCAN
            need_send_signal = True

        last_doc = zone_docs.last()
        # NOTE kostyl :) При ситуации, когда работает два человека с двух терминалов под счетчиком
        # под одним пользователем в одной таске. Необходимо создать таску под второго пользователя,
        # если зона и таска совпадают, создать документ под второго человека. Выдать задание УК.
        if (  # noqa: WPS337
            last_doc
            and zone_docs.count() == 1
            and last_doc.terminal != self.terminal
            and last_doc.counter_scan_task == db_task
        ):
            newtask = Task.objects.create(
                zone=db_task.zone,
                employee=db_employee,
                type=TaskTypeChoices.COUNTER_SCAN,
                status=TaskStatusChoices.WORKED,
                terminal=self.terminal,
            )
            self._add_scanprods_to_task(newtask, srctask.get('scanned_products', []))
            doc = self._create_document(srctask, newtask, db_task.zone, db_employee)
            employee = None
            if self.project.terminal_settings.issuing_task == IssuingTaskChoices.CURRENT_USER:
                employee = Employee.objects.get(pk=srctask['document']['employee'])
            elif self.project.terminal_settings.issuing_task == IssuingTaskChoices.LEAST_LOADED_USER:
                employee = LeastLoadedEmployeeService(
                    project=self.project,
                    role=EmployeeRoleChoices.COUNTER,
                    task_type=TaskTypeChoices.CONTROLLER,
                    exclude_ids=[],
                ).process()

            # Создание задания на С.УК при соблюдении условий автоназначения
            if employee and self.project.auto_assign_enbale and self.project.rmm_settings.auto_zones_amount > 0:
                cctask = Task.objects.create(
                    zone=db_task.zone,
                    employee=employee,
                    type=TaskTypeChoices.COUNTER_CONTROLLER,
                )
                doc.counter_controller_task = cctask
                doc.save()

        match = False
        # Если в зоне есть отработанный УК, и если текущий СКАН совпал с каким-то УК - считать Зону готовой
        zone_controller_tasks = Task.objects.filter(
            zone=db_task.zone,
            type=TaskTypeChoices.CONTROLLER,
        ).exclude(status=TaskStatusChoices.INITIALIZED).order_by('created_at')
        if zone_controller_tasks:
            need_send_signal = True
            newdocument.controller_task = zone_controller_tasks.last()
            for zone_controller_task in zone_controller_tasks:
                if db_task.result == zone_controller_task.result:
                    db_task.status = TaskStatusChoices.SUCCESS_SCAN
                    db_task.zone.status = ZoneStatusChoices.READY
                    zone_controller_task.status = TaskStatusChoices.SUCCESS_SCAN
                    zone_controller_task.save()
                    newdocument.status = DocumentStatusChoices.READY
                    newdocument.color = DocumentColorChoices.GREEN
                    newdocument.controller_task = zone_controller_task
                    newdocument.save()
                    match = True
                    # Проставить всем документам в зоне правильный УК
                    for zone_doc in Document.objects.filter(zone=db_task.zone):
                        zone_doc.controller_task = zone_controller_task
                        zone_doc.save()

        if zone_controller_tasks and not match:
            db_task.status = TaskStatusChoices.FAILED_SCAN
            # Если не совпал ни с каким УК - выдать соответственно настройке
            auto_sett = self.project.rmm_settings.auto_zones_amount > 0
            recalc_dis_sett = self.project.terminal_settings.recalculation_discrepancy
            if recalc_dis_sett == RecalculationDiscrepancyChoices.SCAN:
                if auto_sett:
                    # Если вкл настройки кол-во автоназначаемых зон и выдачи задания на
                    # СКАН - выдать не более 3 раз, если настройка на УК - выдать в любом случае
                    zone_cs_tasks = Task.objects.filter(zone=db_task.zone, type=TaskTypeChoices.COUNTER_SCAN)
                    if zone_cs_tasks.count() < 3:
                        newtask = Task.objects.create(
                            zone=db_task.zone, employee=db_employee, type=TaskTypeChoices.COUNTER_SCAN,
                        )
                else:
                    newtask = Task.objects.create(
                        zone=db_task.zone, employee=db_employee, type=TaskTypeChoices.COUNTER_SCAN,
                    )
            elif recalc_dis_sett == RecalculationDiscrepancyChoices.CONTROLLER:
                Task.objects.create(
                    zone=db_task.zone,
                    employee=zone_controller_tasks.last().employee,
                    type=TaskTypeChoices.CONTROLLER,
                )

        # Нужно присвоить документу последние актуальные задания аудиторов
        auditor_zone_tasks = Task.objects.filter(
            zone=db_task.zone,
            type=TaskTypeChoices.AUDITOR,
        ).exclude(
            status=TaskStatusChoices.INITIALIZED,
        ).order_by('created_at')
        if auditor_zone_tasks:
            newdocument.auditor_task = auditor_zone_tasks.last()
            need_send_signal = True

        auditor_extrnal_zone_tasks = Task.objects.filter(
            zone=db_task.zone,
            type=TaskTypeChoices.AUDITOR_EXTERNAL,
        ).exclude(
            status=TaskStatusChoices.INITIALIZED,
        ).order_by('created_at')
        if auditor_extrnal_zone_tasks:
            newdocument.auditor_external_task = auditor_extrnal_zone_tasks.last()
            need_send_signal = True

        auditor_controller_zone_tasks = Task.objects.filter(
            zone=db_task.zone,
            type=TaskTypeChoices.AUDITOR_CONTROLLER,
        ).exclude(
            status=TaskStatusChoices.INITIALIZED,
        ).order_by('created_at')
        if auditor_controller_zone_tasks:
            newdocument.auditor_controller_task = auditor_controller_zone_tasks.last()
            need_send_signal = True
        newdocument.save()

        if need_send_signal:
            SendWebSocketInfo().send_about_update_documents(documents=[newdocument])

        # Очистить неактуальные задания
        Task.objects.filter(
            zone=db_task.zone, type=TaskTypeChoices.COUNTER_SCAN, status=TaskStatusChoices.INITIALIZED,
        ).exclude(
            pk__in=[newtask.pk] if 'newtask' in locals() else [],
        ).delete()

        db_task.save()
        db_task.zone.save()
        SendWebSocketInfo().send_about_update_zones(zones=[db_task.zone])

    def _process_controller(self, srctask: Dict, db_zone: Zone, db_task: Task):  # noqa: WPS213 WPS231
        """Обработка задания УК."""
        db_task.result = srctask.get('result')
        db_task.status = TaskStatusChoices.WORKED
        db_task.save()

        # Очистить неактуальные задания УК
        Task.objects.filter(
            zone=db_task.zone, type=TaskTypeChoices.CONTROLLER, status=TaskStatusChoices.INITIALIZED,
        ).delete()

        zone_docs = Document.objects.filter(zone=db_zone).order_by('created_at')
        if not zone_docs:
            return

        for zone_doc in zone_docs:
            zone_doc.controller_task = db_task
            zone_doc.save()

        match = False
        for zone_doc in zone_docs:
            if zone_doc.counter_scan_task.result == round(Decimal(db_task.result), 3):
                match = True
                db_zone.status = ZoneStatusChoices.READY
                db_zone.save()
                zone_doc.status = DocumentStatusChoices.READY
                zone_doc.color = DocumentColorChoices.GREEN
                zone_doc.save()
                zone_doc.counter_scan_task.status = TaskStatusChoices.SUCCESS_SCAN
                zone_doc.counter_scan_task.save()
                db_task.status = TaskStatusChoices.SUCCESS_SCAN
                db_task.save()
                # Удалить назначенные задания СКАН если совпало
                Task.objects.filter(
                    zone=db_task.zone, type=TaskTypeChoices.COUNTER_SCAN, status=TaskStatusChoices.INITIALIZED,
                ).delete()
                # Другие документы в зоне - в неготовые
                Document.objects.filter(zone=db_task.zone).exclude(pk=zone_doc.pk).update(
                    status=DocumentStatusChoices.NOT_READY,
                    color=DocumentColorChoices.RED,
                )
            else:
                db_task.status = TaskStatusChoices.FAILED_SCAN
                db_task.save()

        # Если не сошлись, в зависимости от настройки recalculation_discrepancy выдать новое задание + есть условия
        if not match:
            db_task.status = TaskStatusChoices.FAILED_SCAN if zone_docs else TaskStatusChoices.WORKED

            zone_cs_tasks = Task.objects.filter(
                zone=db_zone,
                type=TaskTypeChoices.COUNTER_SCAN,
                status__in=(TaskStatusChoices.WORKED, TaskStatusChoices.SUCCESS_SCAN, TaskStatusChoices.FAILED_SCAN),
            )
            zone_cs_tasks.update(status=TaskStatusChoices.FAILED_SCAN)

            recals_sett = self.project.terminal_settings.recalculation_discrepancy
            if recals_sett == RecalculationDiscrepancyChoices.SCAN:
                # Выбрана настройка СКАН
                if zone_cs_tasks:
                    employee = zone_cs_tasks.order_by('created_at').last().employee
                    Task.objects.create(zone=db_zone, employee=employee, type=TaskTypeChoices.COUNTER_SCAN)
            elif recals_sett == RecalculationDiscrepancyChoices.CONTROLLER:
                # Выбрана настройка УК
                zone_cc_tasks = Task.objects.filter(zone=db_zone, type=db_task.type)
                if not zone_cc_tasks.exclude(pk=db_task.pk):  # noqa: WPS504
                    Task.objects.create(zone=db_zone, employee=db_task.employee, type=db_task.type)
                else:
                    # Если в зоне 1 задание УК, и его результат сходится с тем что пришел - выдать на переСКАН
                    if (  # noqa: WPS337
                        zone_cc_tasks.exclude(pk=db_task.pk).count() == 1
                        and zone_cc_tasks.exclude(pk=db_task.pk).first().result == db_task.result
                        and zone_cs_tasks
                    ):
                        employee = zone_cs_tasks.order_by('created_at').last().employee
                        Task.objects.create(zone=db_zone, employee=employee, type=TaskTypeChoices.COUNTER_SCAN)
                    # Пока заданий УК в зоне меньше чем в 3 раза чем СКАН - выдавать УК, когда ровно в 3 - СКАН
                    if zone_cc_tasks.count() / zone_cs_tasks.count() < 3:
                        Task.objects.create(zone=db_zone, employee=db_task.employee, type=db_task.type)
                    else:
                        Task.objects.create(
                            zone=db_zone,
                            employee=zone_cs_tasks.first().employee,
                            type=TaskTypeChoices.COUNTER_SCAN,
                        )

        SendWebSocketInfo().send_about_update_documents(documents=zone_docs)
        SendWebSocketInfo().send_about_update_zones(zones=[db_zone])

    def _process_auditor(self, srctask: Dict, db_task: Task, zone_docs: QuerySet):
        """Обработка задания АУДИТОР."""
        if Document.objects.filter(zone=db_task.zone, auditor_task=db_task):
            return
        self._add_scanprods_to_task(db_task, srctask.get('scanned_products', []))
        db_task.status = TaskStatusChoices.WORKED
        db_task.save()
        zone_docs.update(auditor_task=db_task)
        SendWebSocketInfo().send_about_update_documents(zone_docs)
        SendWebSocketInfo().send_about_update_zones(zones=[db_task.zone])

    def _process_auditor_controller(self, srctask: Dict, db_task: Task, zone_docs: QuerySet):
        """Обработка задания АУДИТОР.УК."""
        if Document.objects.filter(zone=db_task.zone, auditor_controller_task=db_task):
            return
        db_task.result = srctask.get('result')
        db_task.status = TaskStatusChoices.WORKED
        db_task.save()
        zone_docs.update(auditor_controller_task=db_task)
        SendWebSocketInfo().send_about_update_documents(zone_docs)
        SendWebSocketInfo().send_about_update_zones(zones=[db_task.zone])

    def _process_auditor_ext(self, srctask: Dict, db_task: Task, zone_docs: QuerySet):
        """Обработка задания ВНЕШНИЙ АУДИТОР."""
        if Document.objects.filter(zone=db_task.zone, auditor_external_task=db_task):
            return
        self._add_scanprods_to_task(db_task, srctask.get('scanned_products', []))
        db_task.status = TaskStatusChoices.WORKED
        db_task.save()
        zone_docs.update(auditor_external_task=db_task)
        SendWebSocketInfo().send_about_update_documents(zone_docs)
        SendWebSocketInfo().send_about_update_zones(zones=[db_task.zone])

    def _create_controller_task(self, db_zone: Zone, db_employee: Employee) -> None:
        """
        Функция для текущего переданного задания СКАН автоматически создает соотв. новое задание УК.

        В зависимости от настройки терминала проекта (terminal_settings.issuing_task) при выполнении задачи сканом
        необходимо автоматически создать новое задания для УК, при условии, что у сотрудника нет активного задания
        в зоне. Для настройки Текущий пользователь - в исполнители поставить текущего пользователя, при настройке
        Наименее загруженному пользователю - высчитать наименее загруженного и назначить на него задачу УК.
        Не создавать задания на пользователя, если на него уже есть активное задание в какой-то зоне за УК.
        """
        if self.project.rmm_settings.auto_zones_amount == 0 or not self.project.auto_assign_enbale:
            return

        employee = None
        if self.project.terminal_settings.issuing_task == IssuingTaskChoices.CURRENT_USER:
            employee = db_employee
        elif self.project.terminal_settings.issuing_task == IssuingTaskChoices.LEAST_LOADED_USER:
            employee = LeastLoadedEmployeeService(
                project=self.project,
                role=EmployeeRoleChoices.COUNTER,
                task_type=TaskTypeChoices.CONTROLLER,
                exclude_ids=[db_employee.pk],
            ).process()

        if not employee:
            return

        qs = Task.objects.filter(
            employee=employee,
            type=TaskTypeChoices.CONTROLLER,
            status=TaskStatusChoices.INITIALIZED,
        )
        if qs.count() < self.project.rmm_settings.auto_zones_amount:
            IssuingTasksService(zone=db_zone, employees=[employee], role=TaskTypeChoices.CONTROLLER).process()

    def _make_batch_tasks_counter_scan(self, not_ready_zones, db_task, db_employee):
        counter = 0
        for zone in not_ready_zones:
            if not zone.tasks.filter(type=db_task.type):
                IssuingTasksService(zone=zone, employees=[db_employee], role=db_task.type).process()
                counter += 1
            if counter == self.project.rmm_settings.auto_zones_amount:
                break

    def _make_batch_tasks_controller(self, not_ready_zones, db_task, db_employee):  # noqa: WPS231
        counter = 0
        new_tasks_ids = []
        for zone in not_ready_zones:
            if zone.tasks.filter(type=TaskTypeChoices.COUNTER_SCAN, status=TaskStatusChoices.INITIALIZED):
                # Если в зоне есть активные неотработанные задания СКАН - пропустить
                continue

            if not zone.tasks.filter(type=TaskTypeChoices.COUNTER_SCAN):
                # или если в зоне вообще нет заданий СКАН - тоже пропустить
                continue

            if zone.tasks.filter(type=TaskTypeChoices.CONTROLLER):
                # Если в зоне уже есть задание УК - пропустить
                continue

            # Если в зоне есть отработанное задание СКАН, не назначать на юзера, который делал
            scan_tasks_empl_ids = []
            for zone_task in zone.tasks.filter(type=TaskTypeChoices.COUNTER_SCAN):
                scan_tasks_empl_ids.append(zone_task.employee.pk)

            employee = LeastLoadedEmployeeService(
                project=self.project,
                role=EmployeeRoleChoices.COUNTER,
                task_type=db_task.type,
                exclude_ids=scan_tasks_empl_ids,
            ).process()

            # Пропустить выдачу, если в проекте есть хотя бы одно активное задание УК
            # на этого пользователя. Исключить из проверки новые выданные задания
            exists_empl_controller_tasks = Task.objects.filter(
                zone__project=self.project,
                employee=employee,
                type=TaskTypeChoices.CONTROLLER,
                status=TaskStatusChoices.INITIALIZED,
            ).exclude(
                pk__in=new_tasks_ids,
            )
            if exists_empl_controller_tasks.exists():
                continue

            new_ids = IssuingTasksService(zone=zone, employees=[employee], role=db_task.type).process()
            new_tasks_ids.extend(new_ids)
            counter += 1
            if counter == self.project.rmm_settings.auto_zones_amount:
                break

    def _check_autoassign(self, db_employee: Employee, db_task: Task) -> None:
        """
        Функция проверяет, что СКАН или УК выполнил все свои зоны, и, если включены настройки
        auto_zones_amount и auto_assign_enbale, выдает новую пачку зон на этого СКАН или наименее
        загруженному УК. Не выдавать на УК пользователя который назначен на СКАН в зоне.
        """
        if (  # noqa: WPS337
            self.project.rmm_settings.auto_zones_amount == 0
            or not self.project.auto_assign_enbale
            or db_employee.is_deleted
            or not db_employee.is_auto_assignment
        ):
            return

        if Task.objects.filter(  # noqa: WPS337
            zone__project=self.project,
            employee=db_employee,
            type=db_task.type,
            status=TaskStatusChoices.INITIALIZED,
        ).exists():
            return

        not_ready_zones = Zone.objects.filter(
            project=self.project, status=ZoneStatusChoices.NOT_READY, is_auto_assignment=True,
        ).order_by('serial_number')

        if db_task.type == TaskTypeChoices.COUNTER_SCAN:
            self._make_batch_tasks_counter_scan(not_ready_zones, db_task, db_employee)
        elif db_task.type == TaskTypeChoices.CONTROLLER:
            self._make_batch_tasks_controller(not_ready_zones, db_task, db_employee)
