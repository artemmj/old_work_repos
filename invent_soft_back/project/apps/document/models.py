from django.db import models
from django_lifecycle import LifecycleModel, hook

from apps.employee.models import Employee
from apps.helpers.models import CreatedModel, enum_max_length
from apps.task.models import Task, TaskTypeChoices
from apps.terminal.models import Terminal


class DocumentQuerySet(models.QuerySet):  # noqa: WPS214

    def with_counter_scan_barcode_amount(self):
        return self.annotate(
            counter_scan_barcode_amount=models.Case(
                models.When(
                    counter_scan_task__isnull=False,
                    then=models.F('counter_scan_task__result'),
                ),
                default=0,
                output_field=models.DecimalField(),
            ),
        )

    def with_controller_barcode_amount(self):
        return self.annotate(
            controller_barcode_amount=models.Case(
                models.When(
                    controller_task__isnull=False,
                    then=models.F('controller_task__result'),
                ),
                default=0,
                output_field=models.DecimalField(),
            ),
        )


class DocumentStatusChoices(models.TextChoices):
    READY = 'ready', 'Готов'
    NOT_READY = 'not_ready', 'Не готов'


class DocumentColorChoices(models.TextChoices):
    GREEN = 'green', 'Зеленый'
    RED = 'red', 'Красный'
    GRAY = 'gray', 'Серый'
    ORANGE = 'orange', 'Оранжевый'
    BLUE = 'blue', 'Голубой'
    VIOLET = 'violet', 'Фиолетовый'
    WHITE = 'white', 'Белый'


class Document(CreatedModel, LifecycleModel):
    fake_id = models.IntegerField(default=1)
    employee = models.ForeignKey(
        Employee,
        models.SET_NULL,
        related_name='documents',
        verbose_name='Сотрудник',
        null=True,
        blank=True,
    )
    zone = models.ForeignKey(
        to='zone.Zone',
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name='Зона',
    )
    status = models.CharField(
        'Статус',
        max_length=enum_max_length(DocumentStatusChoices),
        choices=DocumentStatusChoices.choices,
        default=DocumentStatusChoices.NOT_READY,
    )
    start_audit_date = models.DateTimeField(verbose_name='Начало аудита', null=True, blank=True)
    end_audit_date = models.DateTimeField(verbose_name='Окончание аудита', null=True, blank=True)
    tsd_number = models.IntegerField(verbose_name='№ ТСД', null=True, blank=True)
    terminal = models.ForeignKey(Terminal, models.SET_NULL, related_name='document', null=True, blank=True)
    suspicious = models.BooleanField('Подозрительный', default=False)

    color = models.CharField(
        'Цвет',
        max_length=enum_max_length(DocumentColorChoices),
        choices=DocumentColorChoices.choices,
        default=DocumentColorChoices.RED,
    )
    # Необходимо хранить предыдущий цвет документа при ручной установке цвета,
    # это никак не должно влиять на соседние документы в зоне
    prev_color = models.CharField(
        max_length=enum_max_length(DocumentColorChoices),
        choices=DocumentColorChoices.choices,
        default=None,
        null=True,
        blank=True,
    )
    color_changed = models.BooleanField(default=False)

    # Для хранения актуальных задач
    counter_scan_task = models.ForeignKey(
        Task,
        models.SET_NULL,
        related_name='counter_scan_document',
        null=True,
        blank=True,
    )
    controller_task = models.ForeignKey(
        Task,
        models.SET_NULL,
        related_name='controller_document',
        null=True,
        blank=True,
    )
    auditor_task = models.ForeignKey(
        Task,
        models.SET_NULL,
        related_name='auditor_document',
        null=True,
        blank=True,
    )
    auditor_controller_task = models.ForeignKey(
        Task,
        models.SET_NULL,
        related_name='auditor_controller_document',
        null=True,
        blank=True,
    )
    auditor_external_task = models.ForeignKey(
        Task,
        models.SET_NULL,
        related_name='auditor_external_document',
        null=True,
        blank=True,
    )
    storage_task = models.ForeignKey(
        Task,
        models.SET_NULL,
        related_name='storage_document',
        null=True,
        blank=True,
    )
    is_replace_specification = models.BooleanField(
        'Замена спецификации',
        default=False,
    )

    objects = DocumentQuerySet.as_manager()

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

    def __str__(self):
        return f'Документ {self.id} - {self.status}'

    @hook('after_create')
    def generate_fake_id(self):
        last_docs = Document.objects.filter(zone__project=self.zone.project).order_by('fake_id')
        last_doc = last_docs.exclude(pk=self.pk).last()
        if last_doc:
            self.fake_id = last_doc.fake_id + 1  # noqa: WPS601
            self.save()
