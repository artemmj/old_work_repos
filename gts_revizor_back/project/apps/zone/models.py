from django.db import models
from django_lifecycle import AFTER_UPDATE, LifecycleModel, hook

from apps.helpers.models import CreatedModel, UUIDModel, enum_max_length
from apps.project.models import Project
from apps.task.models import Task, TaskStatusChoices, TaskTypeChoices

MAX_ZONE_CODE_LEN = 31


class ZoneQuerySet(models.QuerySet):  # noqa: WPS214

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

    def get_counter_scan_tasks(self):
        return self.prefetch_related(
            models.Prefetch(
                'tasks',
                queryset=(
                    Task
                    .objects
                    .select_related('zone', 'employee', 'terminal')
                    .filter(type=TaskTypeChoices.COUNTER_SCAN)
                    .order_by('-created_at')
                ),
                to_attr='counter_scan_tasks',
            ),
        )

    def get_counter_scan_tasks_status(self):
        return self.prefetch_related(
            models.Prefetch(
                'tasks',
                queryset=(
                    Task
                    .objects
                    .select_related('zone', 'employee', 'terminal')
                    .filter(
                        type=TaskTypeChoices.COUNTER_SCAN,
                        status__in=(
                            TaskStatusChoices.WORKED,
                            TaskStatusChoices.SUCCESS_SCAN,
                            TaskStatusChoices.FAILED_SCAN,
                        ),
                    )
                ),
                to_attr='counter_scan_tasks_status',
            ),
        )

    def get_controller_tasks(self):
        return self.prefetch_related(
            models.Prefetch(
                'tasks',
                queryset=(
                    Task
                    .objects
                    .select_related('zone', 'employee', 'terminal')
                    .filter(type=TaskTypeChoices.CONTROLLER)
                    .order_by('-created_at')
                ),
                to_attr='controller_tasks',
            ),
        )

    def get_controller_tasks_status(self):
        return self.prefetch_related(
            models.Prefetch(
                'tasks',
                queryset=(
                    Task
                    .objects
                    .select_related('zone', 'employee', 'terminal')
                    .filter(
                        type=TaskTypeChoices.CONTROLLER,
                        status__in=(
                            TaskStatusChoices.WORKED,
                            TaskStatusChoices.SUCCESS_SCAN,
                            TaskStatusChoices.FAILED_SCAN,
                        ),
                    )
                ),
                to_attr='controller_tasks_status',
            ),
        )

    def get_auditor_tasks(self):
        return self.prefetch_related(
            models.Prefetch(
                'tasks',
                queryset=(
                    Task
                    .objects
                    .select_related('zone', 'employee', 'terminal')
                    .filter(type=TaskTypeChoices.AUDITOR)
                    .order_by('-created_at')
                ),
                to_attr='auditor_tasks',
            ),
        )

    def get_auditor_tasks_status(self):
        return self.prefetch_related(
            models.Prefetch(
                'tasks',
                queryset=(
                    Task
                    .objects
                    .select_related('zone', 'employee', 'terminal')
                    .filter(
                        type=TaskTypeChoices.AUDITOR,
                        status__in=(
                            TaskStatusChoices.WORKED,
                            TaskStatusChoices.SUCCESS_SCAN,
                            TaskStatusChoices.FAILED_SCAN,
                        ),
                    )
                ),
                to_attr='auditor_tasks_status',
            ),
        )

    def get_auditor_controller_tasks(self):
        return self.prefetch_related(
            models.Prefetch(
                'tasks',
                queryset=(
                    Task
                    .objects
                    .select_related('zone', 'employee', 'terminal')
                    .filter(type=TaskTypeChoices.AUDITOR_CONTROLLER)
                    .order_by('-created_at')
                ),
                to_attr='auditor_controller_tasks',
            ),
        )

    def get_auditor_controller_tasks_status(self):
        return self.prefetch_related(
            models.Prefetch(
                'tasks',
                queryset=(
                    Task
                    .objects
                    .select_related('zone', 'employee', 'terminal')
                    .filter(
                        type=TaskTypeChoices.AUDITOR_CONTROLLER,
                        status__in=(
                            TaskStatusChoices.WORKED,
                            TaskStatusChoices.SUCCESS_SCAN,
                            TaskStatusChoices.FAILED_SCAN,
                        ),
                    )
                ),
                to_attr='auditor_controller_tasks_status',
            ),
        )

    def get_auditor_external_controller_tasks(self):
        return self.prefetch_related(
            models.Prefetch(
                'tasks',
                queryset=(
                    Task
                    .objects
                    .select_related('zone', 'employee', 'terminal')
                    .filter(type=TaskTypeChoices.AUDITOR_EXTERNAL)
                    .order_by('-created_at')
                ),
                to_attr='auditor_external_controller_tasks',
            ),
        )

    def get_auditor_external_controller_tasks_status(self):
        return self.prefetch_related(
            models.Prefetch(
                'tasks',
                queryset=(
                    Task
                    .objects
                    .select_related('zone', 'employee', 'terminal')
                    .filter(
                        type=TaskTypeChoices.AUDITOR_EXTERNAL,
                        status__in=(
                            TaskStatusChoices.WORKED,
                            TaskStatusChoices.SUCCESS_SCAN,
                            TaskStatusChoices.FAILED_SCAN,
                        ),
                    )
                ),
                to_attr='auditor_external_controller_tasks_status',
            ),
        )

    def get_storage_tasks(self):
        return self.prefetch_related(
            models.Prefetch(
                'tasks',
                queryset=(
                    Task
                    .objects
                    .select_related('zone', 'employee', 'terminal')
                    .filter(type=TaskTypeChoices.STORAGE)
                    .order_by('-created_at')
                ),
                to_attr='storage_tasks',
            ),
        )

    def get_storage_tasks_status(self):
        return self.prefetch_related(
            models.Prefetch(
                'tasks',
                queryset=(
                    Task
                    .objects
                    .select_related('zone', 'employee', 'terminal')
                    .filter(
                        type=TaskTypeChoices.STORAGE,
                        status__in=(
                            TaskStatusChoices.WORKED,
                            TaskStatusChoices.SUCCESS_SCAN,
                            TaskStatusChoices.FAILED_SCAN,
                        ),
                    )
                ),
                to_attr='storage_tasks_status',
            ),
        )

    def check_is_one_employee_to_zone(self, value: str, task_type: TaskTypeChoices):
        return self.annotate(
            all_tasks_count=models.Count(
                'tasks',
                filter=models.Q(tasks__type=task_type),
                distinct=True,
            ),
            tasks_count=models.Count(
                'tasks',
                filter=models.Q(
                    tasks__employee__username__exact=value,
                    tasks__type=task_type,
                ),
                distinct=True,
            ),
            is_one_employee_to_zone=models.Case(
                models.When(tasks_count=models.F('all_tasks_count'), then=True),
                default=False,
                output_field=models.BooleanField(),
            ),
            all_tasks_count_filter_status=models.Count(
                'tasks',
                filter=models.Q(
                    tasks__type=task_type,
                    tasks__status__in=(
                        TaskStatusChoices.WORKED,
                        TaskStatusChoices.SUCCESS_SCAN,
                        TaskStatusChoices.FAILED_SCAN,
                    ),
                ),
                distinct=True,
            ),
            is_tasks=models.Case(
                models.When(all_tasks_count_filter_status=0, then=False),
                default=True,
                output_field=models.BooleanField(),
            ),
        )


class ZoneStatusChoices(models.TextChoices):
    READY = 'ready', 'Готова'
    NOT_READY = 'not_ready', 'Не готова'


class Zone(LifecycleModel, UUIDModel, CreatedModel):
    project = models.ForeignKey(Project, verbose_name='Проект', related_name='zones', on_delete=models.CASCADE)
    title = models.CharField('Название', max_length=30, blank=True)
    serial_number = models.PositiveSmallIntegerField('Порядковый номер')
    storage_name = models.CharField('Название склада', max_length=200)
    code = models.CharField('Код зоны', max_length=MAX_ZONE_CODE_LEN, null=True, blank=True)
    status = models.CharField(
        'Статус',
        max_length=enum_max_length(ZoneStatusChoices),
        choices=ZoneStatusChoices.choices,
        default=ZoneStatusChoices.NOT_READY,
    )
    is_auto_assignment = models.BooleanField('Автоназначение', default=True)

    objects = ZoneQuerySet().as_manager()

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

    @hook(AFTER_UPDATE)
    def send_socket_update_zone(self):
        from apps.websocket.services import SendWebSocketService  # noqa: WPS433
        SendWebSocketService().send_about_update_zones(zones=[self])
