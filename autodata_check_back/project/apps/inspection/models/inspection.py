from typing import Final

from _decimal import Decimal  # noqa: WPS436
from constance import config
from django.db import models
from django.utils import timezone
from django_lifecycle import LifecycleModelMixin, hook

from apps.helpers.models import CreatedModel, UpdatedModel, UUIDModel, enum_max_length
from apps.inspection_task.models.task import InspectorTaskStatuses
from apps.template.models import Template
from apps.transaction.models import OrganizationTransaction, OrganizationTransactionOperations
from apps.transaction.models.abstract import TransactionTypes

_FIELD_MAX_LENGTH: Final = 40


class StatusChoices(models.TextChoices):
    COMPLETE = 'complete', 'Завершен'
    TROUBLESHOOTING = 'troubleshooting', 'Устранение недочетов'
    UNDER_REVIEW = 'under_review', 'На проверке'
    ACCEPTED = 'accepted', 'Принят'
    DRAFT = 'draft', 'Черновик'


class InspectionTypes(models.TextChoices):
    SELF_INSPECTION = 'self_inspection', 'Самостоятельный'
    BY_TASK = 'by_task', 'По заданию'
    BY_TASK_WITH_ORGANIZATION_INSPECTOR = 'by_task_with_organization_inspector', 'По заданию с инспектором организации'


class Inspection(LifecycleModelMixin, UUIDModel, CreatedModel, UpdatedModel):  # noqa: WPS214
    inspector = models.ForeignKey(
        'user.User',
        verbose_name='Инспектор осмотра',
        related_name='inspections',
        on_delete=models.PROTECT,
    )
    organization = models.ForeignKey(
        'organization.Organization',
        verbose_name='Организация',
        related_name='inspections',
        on_delete=models.PROTECT,
    )
    task = models.ForeignKey(
        'inspection_task.InspectionTask',
        verbose_name='Задание на осмотр',
        related_name='inspections',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    status = models.CharField(
        'Статус осмотра',
        max_length=enum_max_length(StatusChoices),
        choices=StatusChoices.choices,
        default=StatusChoices.DRAFT,
    )
    address = models.ForeignKey(
        'address.Address',
        verbose_name='Адрес',
        related_name='inspections',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    comment = models.TextField('Комментарий', null=True, blank=True)
    template = models.ForeignKey(
        Template,
        verbose_name='Шаблон осмотра',
        related_name='inspections',
        on_delete=models.SET_NULL,
        null=True,
    )
    complete_date = models.DateTimeField('Дата завершения', null=True, blank=True, auto_now=True)
    is_public = models.BooleanField('Публичный', default=False)
    type = models.CharField(
        'Тип',
        max_length=enum_max_length(InspectionTypes),
        choices=InspectionTypes.choices,
        default=InspectionTypes.SELF_INSPECTION,
    )
    fake_deleted = models.BooleanField('Удален только для фронта', default=False)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Осмотр'
        verbose_name_plural = 'Осмотры'

    def __str__(self):
        return str(self.id)

    def complete_task(self):
        """Смена статуса задания на осмотр выполнен после завершения всех осмотров."""
        complete_inspections_by_task = Inspection.objects.filter(
            task_id=self.task_id, status=StatusChoices.COMPLETE,
        ).count()
        if self.task and complete_inspections_by_task == self.task.inspection_task_cars.count():
            self.task.status = InspectorTaskStatuses.INSPECTION_DONE
            self.task.save()

    def paid_task(self):
        """Смена статуса задания на оплачено после принятия всех осмотров."""
        accepted_inspections_by_task = Inspection.objects.filter(
            task_id=self.task_id, status=StatusChoices.ACCEPTED,
        ).count()
        if self.task and accepted_inspections_by_task == self.task.inspection_task_cars.count():
            self.task.status = InspectorTaskStatuses.PAID
            self.task.save()

    def withdraw_by_self_inspection(self):
        """Создание транзакции после завершения самостоятельного осмотра."""
        if (  # noqa: WPS337
            not self.task
            and self.organization
            and self.inspector
            and not self.organization.subscriptions.filter(is_active=True).exists()
        ):
            amount = Decimal(config.SELF_INSPECTION_PRICE)
            if self.organization.self_inspection_price:
                amount = self.organization.self_inspection_price
            OrganizationTransaction.objects.create(
                organization=self.organization,
                user=self.inspector,
                type=TransactionTypes.WITHDRAW,
                operation=OrganizationTransactionOperations.SELF_INSPECTION,
                amount=amount,
            )

    @hook('after_update', when='status', is_now=StatusChoices.COMPLETE)
    def complete_inspection(self):
        self.complete_date = timezone.now()  # noqa: WPS601
        self.complete_task()
        self.withdraw_by_self_inspection()

    @hook('after_update', when='status', is_now=StatusChoices.ACCEPTED)
    def accepted_inspection(self):
        self.paid_task()

    @hook('after_update', when='status', is_now=StatusChoices.TROUBLESHOOTING)
    def troubleshooting_inspection(self):
        if self.task:
            self.task.status = InspectorTaskStatuses.TROUBLESHOOTING
            self.task.save()

    @hook('after_create')
    def after_create(self):
        if self.type == InspectionTypes.SELF_INSPECTION:
            self.is_public = True  # noqa: WPS601
        self.complete_task()

    @hook('after_update')
    def update_date(self):
        self.updated_at = timezone.now()
