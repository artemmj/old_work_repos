from django.db import models

from apps.employee.models import Employee
from apps.helpers.models import CreatedModel, UUIDModel
from apps.project.models import Project


class Terminal(UUIDModel, CreatedModel):
    project = models.ForeignKey(Project, verbose_name='Проект', related_name='terminals', on_delete=models.CASCADE)
    employee = models.OneToOneField(
        Employee,
        models.SET_NULL,
        related_name='terminal',
        verbose_name='Сотрудник',
        null=True,
        blank=True,
    )
    number = models.PositiveIntegerField('Номер')
    ip_address = models.GenericIPAddressField('IP адрес')
    db_loading = models.BooleanField('Загрузка БД', default=False)
    last_connect = models.DateTimeField('Дата/Время последнего коннекта', null=True, blank=True)
    mac_address = models.CharField('Мак адрес', max_length=50, blank=True, null=True)
    device_model = models.CharField('Модель терминала', max_length=50, blank=True, null=True)

    class Meta:
        ordering = ('number',)
        verbose_name = 'Терминал'
        verbose_name_plural = 'Терминалы'
        constraints = [
            models.UniqueConstraint(
                fields=['project', 'number'],
                name='Номер терминала в рамках проекта',
            ),
        ]

    def __str__(self):
        return f'Терминал {self.number}'
