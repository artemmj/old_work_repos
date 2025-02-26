from django.db import models
from django_lifecycle import LifecycleModel

from apps.helpers.model_fields import ChoiceArrayField
from apps.helpers.models import CreatedModel, UUIDModel, enum_max_length
from apps.project.models import Project


class EmployeeRoleChoices(models.TextChoices):
    COUNTER = 'counter', 'Счетчик'  # Счетчик и УК
    AUDITOR = 'auditor', 'Аудитор'  # Аудитор и Аудитор УК
    AUDITOR_EXTERNAL = 'auditor_external', 'Внешний аудитор'
    STORAGE = 'storage', 'Сотрудник склада'


class Employee(UUIDModel, LifecycleModel, CreatedModel):
    project = models.ForeignKey(Project, verbose_name='Проект', related_name='employees', on_delete=models.CASCADE)
    username = models.CharField('Имя', max_length=150, blank=True)
    serial_number = models.PositiveSmallIntegerField('Порядковый номер', null=True, blank=True)
    roles = ChoiceArrayField(
        models.CharField(
            'Роль',
            max_length=enum_max_length(EmployeeRoleChoices),
            choices=EmployeeRoleChoices.choices,
        ),
        verbose_name='Роли',
    )
    is_deleted = models.BooleanField(default=False)
    is_auto_assignment = models.BooleanField('Автоназначение', default=False)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        constraints = [
            models.UniqueConstraint(
                fields=['project', 'serial_number'],
                name='Порядковый номер сотрудника в рамках проекта',
            ),
        ]

    def __str__(self):
        return self.username
