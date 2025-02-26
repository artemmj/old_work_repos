from datetime import datetime
from decimal import Decimal
from typing import Final

from constance import config
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.timezone import now
from django_lifecycle import LifecycleModelMixin, hook
from phonenumber_field.modelfields import PhoneNumberField

from apps.car.models import Brand, Category, Model
from apps.devices.tasks import send_push
from apps.helpers.models import CreatedModel, UUIDModel, enum_max_length
from apps.inspection_task.models.search import InspectionTaskSearch
from apps.inspection_task.services.activate_searching import ActivateSearchingService
from apps.notification.models import (
    InspectorAddBalanceNotification,
    TaskAcceptedNotification,
    TaskCompletedNotification,
    TaskFixOrganizationInspectorNotification,
    TaskFixServiceInspectorNotification,
)
from apps.transaction.models import (
    InspectorTransaction,
    InspectorTransactionOperations,
    OrganizationTransaction,
    OrganizationTransactionOperations,
)
from apps.transaction.models.abstract import TransactionTypes

_FIELD_MAX_LENGTH: Final = 100


class InspectorTaskStatuses(models.TextChoices):
    DRAFT = 'draft', 'Черновик'
    INSPECTOR_SEARCH = 'inspector_search', 'Поиск инспектора'
    TASK_ACCEPTED = 'task_accepted', 'Задание принято'
    INSPECTION_APPOINTED = 'inspection_appointed', 'Назначен осмотр'
    INSPECTION_DATE_CONFIRMED = 'inspection_date_confirmed', 'Дата осмотра подтверждена'
    TROUBLESHOOTING = 'troubleshooting', 'Устранение недочетов'
    INSPECTION_DONE = 'inspection_done', 'Осмотр выполнен'
    PAID = 'paid', 'Оплачено'


class InspectorTaskTypes(models.TextChoices):
    FOR_SEARCH_INSPECTOR = 'for_search_inspector', 'Для поиска инспектора'
    FOR_APPOINTMENT = 'for_appointment', 'Для назначения инспектора организации'


class InspectionTask(LifecycleModelMixin, UUIDModel, CreatedModel):   # noqa: WPS214, WPS338
    author = models.ForeignKey(
        'user.User',
        verbose_name='Автор',
        related_name='author_inspection_tasks',
        on_delete=models.CASCADE,
    )
    inspector = models.ForeignKey(
        'user.User',
        verbose_name='Инспектор осмотра',
        related_name='inspector_inspection_tasks',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    organization = models.ForeignKey(
        'organization.Organization',
        verbose_name='Организация',
        related_name='inspection_tasks',
        on_delete=models.CASCADE,
    )
    fio = models.CharField('ФИО контактного лица', max_length=_FIELD_MAX_LENGTH)
    phone = PhoneNumberField('Номер телефона контактного лица', help_text='Пример, +79510549236')
    address = models.ForeignKey(
        'address.Address',
        verbose_name='Адрес',
        related_name='inspection_tasks',
        on_delete=models.CASCADE,
    )
    start_date = models.DateField('Дата начала осмотра')
    end_date = models.DateField('Дата конца осмотра')
    accepted_datetime = models.DateTimeField('Дата и время принятия задания', null=True, blank=True)
    planed_date = models.DateField('Плановая дата осмотра', null=True, blank=True)
    planed_date_confirm = models.BooleanField('Дата осмотра подтверждена', default=False)
    status = models.CharField(
        'Статус',
        max_length=enum_max_length(InspectorTaskStatuses),
        choices=InspectorTaskStatuses.choices,
        default=InspectorTaskStatuses.DRAFT,
    )
    last_status_change_date = models.DateTimeField('Дата последнего изменения статуса', null=True)
    type = models.CharField(
        'Тип',
        max_length=enum_max_length(InspectorTaskTypes),
        choices=InspectorTaskTypes.choices,
        default=InspectorTaskTypes.FOR_SEARCH_INSPECTOR,
    )
    is_accrual = models.BooleanField('Начислено инспектору', default=False)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Задание на осмотр'
        verbose_name_plural = 'Задания на осмотр'

    @property
    def inspector_amount(self):
        """Кол-во средств которое получит инспектор по выполнению задания."""
        price = float(self.address.city.inspection_price)
        cars = self.inspection_task_cars.all().count()
        percent = config.INSPECTOR_PERCENT
        return '%.2f' % Decimal(price * cars * (percent / 100))  # noqa: WPS323

    @property
    def organization_amount(self):
        """Кол-во средств которое спишется с организации."""
        price = float(self.address.city.inspection_price)
        cars = self.inspection_task_cars.all().count()
        return '%.2f' % Decimal(price * cars)  # noqa: WPS323

    @hook('after_create')
    def create_search_obj(self):
        """Создание объекта поиска инспектора."""
        InspectionTaskSearch.objects.create(task=self)

    def withdraw_organization(self):
        """Списать с организации."""
        if not self.organization.subscriptions.filter(is_active=True).exists():
            OrganizationTransaction.objects.create(
                organization=self.organization,
                user=self.author,
                type=TransactionTypes.WITHDRAW,
                operation=OrganizationTransactionOperations.INSPECTION_TASK,
                amount=Decimal(self.organization_amount),
            )

    def refund(self):
        """Возврат средств организации."""
        if not self.organization.subscriptions.filter(is_active=True).exists():
            OrganizationTransaction.objects.create(
                organization=self.organization,
                user=self.author,
                type=TransactionTypes.ADD,
                operation=OrganizationTransactionOperations.REFUND_CANCELED_TASK,
                amount=Decimal(self.organization_amount),
            )

    def add_by_task_complete(self):  # noqa: WPS210
        """Начислить деньги инспектору за выполненное задание на осмотр."""
        inspector = self.inspector.inspectors.first()
        if inspector and self.type == InspectorTaskTypes.FOR_SEARCH_INSPECTOR and not self.is_accrual:
            InspectorTransaction.objects.create(
                inspector=inspector,
                type=TransactionTypes.ADD,
                operation=InspectorTransactionOperations.COMPLETED_TASK,
                amount=Decimal(self.inspector_amount),
            )
            self.is_accrual = True  # noqa: WPS601
            self.save()
            # После отправки денег - уведомление инспектору
            amount = '{0:,}'.format(round(float(self.inspector_amount), 0)).replace(',', ' ')  # noqa: WPS221
            message = config.INSPECTOR_MONEY_CAME.replace('[ ]', f'+{amount}')
            notification = InspectorAddBalanceNotification.objects.create(
                user=self.inspector,
                message=message,
            )
            task_car = self.inspection_task_cars.first()
            push_data = {
                'push_type': 'InspectorAddBalanceNotification',
                'notification_id': str(notification.id),
                'brand': task_car.brand.title if task_car else None,
                'model': task_car.model.title if task_car else None,
                'vin': task_car.vin_code if task_car else None,
            }
            send_push.delay(str(self.inspector_id), message, push_data)

    @hook('before_update', when='status', has_changed=True)
    def before_update_status(self):  # noqa: WPS213 WPS231 WPS210
        self.last_status_change_date = now()  # noqa: WPS601

        if self.status == InspectorTaskStatuses.DRAFT:
            self.inspector = None  # noqa: WPS601
            self.planed_date = None  # noqa: WPS601
            self.accepted_datetime = None  # noqa: WPS601
            self.refund()
        if self.status == InspectorTaskStatuses.INSPECTOR_SEARCH:
            if self.inspection_task_search:
                ActivateSearchingService(self.inspection_task_search).process()
            self.withdraw_organization()
        if self.status == InspectorTaskStatuses.TASK_ACCEPTED:
            from apps.inspection_task.services.deactivate_searching import \
                DeactivateSearchingService  # noqa: WPS433, I001
            from apps.inspection_task.services.delete_invitations import DeleteInvitationsService  # noqa: WPS433
            if self.inspection_task_search:
                DeactivateSearchingService(self.inspection_task_search).process()
                DeleteInvitationsService(self, inspector=self.inspector).process()
            self.accepted_datetime = now()  # noqa: WPS601
            # Cоздать новый осмотр
            from apps.inspection_task.services.create_inspections import CreateInspectionsService  # noqa: WPS433
            CreateInspectionsService(self).process()
            if self.type == InspectorTaskTypes.FOR_APPOINTMENT:
                self.withdraw_organization()
            # Создать уведомление автору о принятии инспектором задания
            message = config.TASK_ACCEPTED_BY_INSPECTOR
            date = datetime.now().strftime('%H:%M:%S')
            message += f'\r\n\r\nДата принятия: {date}'  # noqa: WPS336
            TaskAcceptedNotification.objects.create(user=self.author, message=message, inspection_task=self)
        if self.status == InspectorTaskStatuses.TROUBLESHOOTING:
            if self.type == InspectorTaskTypes.FOR_APPOINTMENT:
                # Для инспектора организации
                notification_model = TaskFixOrganizationInspectorNotification
                message = config.INSPECTION_ORGANIZATION_INSPECTOR_NEED_FIXES
                push_type = 'TaskFixOrganizationInspectorNotification'
            elif self.type == InspectorTaskTypes.FOR_SEARCH_INSPECTOR:
                # Для инспектора сервиса
                notification_model = TaskFixServiceInspectorNotification
                message = config.INSPECTION_SERVICE_INSPECTOR_NEED_FIXES
                push_type = 'TaskFixServiceInspectorNotification'

            notification = notification_model.objects.create(
                user=self.inspector,
                message=message,
                inspection_task=self,
            )
            task_car = self.inspection_task_cars.first()
            push_data = {
                'push_type': push_type,
                'inspection_task': str(self.id),
                'notification_id': str(notification.id),
                'brand': task_car.brand.title if task_car else None,
                'model': task_car.model.title if task_car else None,
                'vin': task_car.vin_code if task_car else None,
            }
            send_push.delay(str(self.inspector_id), message, push_data)
        if self.status == InspectorTaskStatuses.PAID:
            self.add_by_task_complete()
            message = config.INSPECTION_COMPLETE
            date = datetime.now().strftime('%H:%M:%S')
            message += f'\r\n\r\nДата выполнения: {date}'  # noqa: WPS336
            notification = TaskCompletedNotification.objects.create(
                user=self.author,
                message=message,
                inspection_task=self,
            )
            push_data = {
                'push_type': 'TaskCompletedNotification',
                'inspection_task': str(self.id),
                'notification_id': str(notification.id),
            }
            send_push.delay(str(self.author_id), message, push_data)

    @hook(
        'after_update',
        when='status',
        was=InspectorTaskStatuses.INSPECTOR_SEARCH,
        is_now=InspectorTaskStatuses.DRAFT,
    )
    def deactivate_searching(self):
        """Выключение поиска инспектора."""
        from apps.inspection_task.services.deactivate_searching import DeactivateSearchingService  # noqa: WPS433, I001
        from apps.inspection_task.services.delete_invitations import DeleteInvitationsService  # noqa: WPS433
        if self.inspection_task_search:
            DeactivateSearchingService(self.inspection_task_search).process()
            DeleteInvitationsService(self).process()


class InspectionTaskCar(UUIDModel):
    serial_number = models.PositiveSmallIntegerField('Порядковый номер', validators=[MinValueValidator(1)])
    category = models.ForeignKey(
        Category,
        verbose_name='Тип ТС',
        related_name='inspection_task_cars',
        on_delete=models.CASCADE,
    )
    brand = models.ForeignKey(
        Brand,
        verbose_name='Марка',
        related_name='inspection_task_cars',
        on_delete=models.CASCADE,
    )
    model = models.ForeignKey(
        Model,
        verbose_name='Модель',
        related_name='inspection_task_cars',
        on_delete=models.CASCADE,
    )
    vin_code = models.CharField('VIN-номер', max_length=_FIELD_MAX_LENGTH)
    unstandart_vin = models.BooleanField('Нестандартный VIN', default=False)
    inspection = models.OneToOneField(
        'inspection.Inspection',
        verbose_name='Осмотр',
        related_name='inspection_task_cars',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    task = models.ForeignKey(
        InspectionTask,
        verbose_name='Задание на осмотр',
        related_name='inspection_task_cars',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('serial_number',)
        verbose_name = 'Авто задания на осмотр'
        verbose_name_plural = 'Авто задания на осмотр'
        unique_together = ['serial_number', 'task']
