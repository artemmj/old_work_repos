from django.db import models
from django_lifecycle import LifecycleModel

from apps.employee.models import Employee
from apps.helpers.models import CreatedModel, UUIDModel, enum_max_length
from apps.terminal.models import Terminal


class TaskTypeChoices(models.TextChoices):
    COUNTER_SCAN = 'counter_scan', 'Счетчик'
    CONTROLLER = 'controller', 'УК'
    AUDITOR = 'auditor', 'Аудитор'
    AUDITOR_CONTROLLER = 'auditor_controller', 'Аудитор УК'
    AUDITOR_EXTERNAL = 'auditor_external', 'Внешний Аудитор'
    STORAGE = 'storage', 'Сотрудник склада'


class TaskStatusChoices(models.TextChoices):
    INITIALIZED = 'initialized', 'Инициализирована для работы'
    WORKED = 'worked', 'Проведена работа'
    FAILED_SCAN = 'failed_scan', 'Неудачный скан, не сошлось'
    SUCCESS_SCAN = 'success_scan', 'Удачный скан, сошлось'


class Task(LifecycleModel, UUIDModel, CreatedModel):
    zone = models.ForeignKey(
        'zone.Zone',
        verbose_name='Зона',
        related_name='tasks',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    employee = models.ForeignKey(
        Employee,
        verbose_name='Сотрудник',
        related_name='tasks',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    type = models.CharField('Тип', max_length=enum_max_length(TaskTypeChoices), choices=TaskTypeChoices.choices)
    status = models.CharField(
        'Статус',
        max_length=23,
        choices=TaskStatusChoices.choices,
        default=TaskStatusChoices.INITIALIZED,
    )
    result = models.DecimalField('Результат', max_digits=11, decimal_places=3, default=0)
    terminal = models.ForeignKey(
        Terminal, verbose_name='Терминал', related_name='tasks', on_delete=models.SET_NULL, null=True, blank=True,
    )

    class Meta:
        ordering = ('-created_at', 'zone')
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'

    def __str__(self):
        return f'Task {self.pk} {self.type}; res: {self.result}; status: {self.status}'

    @property
    def unique_barcodes_count(self):
        return self.scanned_products.count()
