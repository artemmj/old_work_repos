from django.db import models
from django_lifecycle import LifecycleModel

from apps.document.models import Document, DocumentStatusChoices
from apps.employee.models import Employee
from apps.helpers.models import CreatedModel, UUIDModel, enum_max_length
from apps.project.models import Project
from apps.task.models import Task, TaskStatusChoices, TaskTypeChoices

MAX_ZONE_CODE_LEN = 31


class MakeArray(models.Func):
    function = 'ARRAY'


class ZoneQuerySet(models.QuerySet):  # noqa: WPS214

    def calculate_tasks_scanned_products_count(self):
        subquery = models.Subquery(
            Task.objects.filter(
                zone=models.OuterRef('id'),
                type=TaskTypeChoices.COUNTER_SCAN,
                status__in={
                    TaskStatusChoices.WORKED,
                    TaskStatusChoices.SUCCESS_SCAN,
                    TaskStatusChoices.FAILED_SCAN,
                },
            )
            .values('zone')
            .annotate(scanned_products_count=models.Count('scanned_products'))
            .values('scanned_products_count'),
        )
        return self.annotate(
            tasks_scanned_products_count=models.functions.Coalesce(subquery, 0),
        )

    def calculate_barcode_amount(self):
        success_task = Task.objects.filter(
            zone=models.OuterRef('id'),
            type=TaskTypeChoices.COUNTER_SCAN,
            status=TaskStatusChoices.SUCCESS_SCAN,
        ).order_by('-created_at')

        failed_tasks = Task.objects.filter(
            zone=models.OuterRef('id'),
            type=TaskTypeChoices.COUNTER_SCAN,
            status=TaskStatusChoices.FAILED_SCAN,
        ).order_by('-created_at')

        return self.annotate(
            barcode_amount_success_task=models.Subquery(
                queryset=success_task.values('result')[:1],
                output_field=models.DecimalField(),
            ),
            barcode_amount_failed_task=models.Subquery(
                queryset=failed_tasks.values('result')[:1],
                output_field=models.DecimalField(),
            ),
            barcode_amount=models.Case(
                models.When(
                    barcode_amount_success_task__isnull=False,
                    then=models.F('barcode_amount_success_task'),
                ),
                models.When(
                    barcode_amount_failed_task__isnull=False,
                    then=models.F('barcode_amount_failed_task'),
                ),
                default=0,
                output_field=models.DecimalField(),
            ),
        )

    def with_usernames_of_counter_scans(self):
        return self.annotate(
            counter_scans=MakeArray(
                models.Subquery(
                    (
                        Task
                        .objects
                        .select_related('employee')
                        .filter(
                            type=TaskTypeChoices.COUNTER_SCAN,
                            zone_id=models.OuterRef('id'),
                        )
                    )
                    .values('employee__username'),
                ),
            ),
        )

    def with_usernames_of_controllers(self):
        return self.annotate(
            controllers=MakeArray(
                models.Subquery(
                    (
                        Task
                        .objects
                        .select_related('employee')
                        .filter(
                            type=TaskTypeChoices.CONTROLLER,
                            zone_id=models.OuterRef('id'),
                        )
                    )
                    .values('employee__username'),
                ),
            ),
        )

    def check_is_one_counter_scan_to_zone(self, value: str):
        return self.annotate(
            all_tasks_count=models.Count(
                'tasks',
                filter=models.Q(tasks__type=TaskTypeChoices.COUNTER_SCAN),
                distinct=True,
            ),
            counter_scan_tasks_count=models.Count(
                'tasks',
                filter=models.Q(
                    tasks__employee__username__iexact=value,
                    tasks__type=TaskTypeChoices.COUNTER_SCAN,
                ),
                distinct=True,
            ),
            is_one_counter_scan_to_zone=models.Case(
                models.When(counter_scan_tasks_count=models.F('all_tasks_count'), then=True),
                default=False,
                output_field=models.BooleanField(),
            ),
        )

    def check_is_one_controller_to_zone(self, value: str):
        return self.annotate(
            all_controller_tasks_count=models.Count(
                'tasks',
                filter=models.Q(tasks__type=TaskTypeChoices.CONTROLLER),
                distinct=True,
            ),
            controller_tasks_count=models.Count(
                'tasks',
                filter=models.Q(
                    tasks__employee__username__iexact=value,
                    tasks__type=TaskTypeChoices.CONTROLLER,
                ),
                distinct=True,
            ),
            is_one_controller_to_zone=models.Case(
                models.When(controller_tasks_count=models.F('all_controller_tasks_count'), then=True),
                default=False,
                output_field=models.BooleanField(),
            ),
        )


class ZoneStatusChoices(models.TextChoices):
    READY = 'ready', 'Готова'
    NOT_READY = 'not_ready', 'Не готова'


class Zone(LifecycleModel, UUIDModel, CreatedModel):
    project = models.ForeignKey(Project, verbose_name='Проект', related_name='zones', on_delete=models.CASCADE)
    title = models.CharField('Название', max_length=30, blank=True)
    serial_number = models.PositiveIntegerField('Порядковый номер')
    storage_name = models.CharField('Название склада', max_length=200)
    code = models.CharField('Код зоны', max_length=MAX_ZONE_CODE_LEN, null=True, blank=True)
    status = models.CharField(
        'Статус',
        max_length=enum_max_length(ZoneStatusChoices),
        choices=ZoneStatusChoices.choices,
        default=ZoneStatusChoices.NOT_READY,
    )
    is_auto_assignment = models.BooleanField('Автоназначение', default=True)

    objects = ZoneQuerySet.as_manager()

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Зона'
        verbose_name_plural = 'Зоны'
        constraints = [
            models.UniqueConstraint(
                fields=['project', 'serial_number'],
                name='Порядковый номер зоны в рамках проекта',
            ),
        ]

    def __str__(self):
        return self.title

    def save(self, generate_code=False, *args, **kwargs):
        if generate_code:
            proj_zones = Zone.objects.filter(project=self.project).order_by('code')
            if not proj_zones:  # noqa: WPS504
                self.code = 1  # noqa: WPS601
            else:
                self.code = int(proj_zones.last().code) + 1  # noqa: WPS601  # TODO

        return super().save(*args, **kwargs)
