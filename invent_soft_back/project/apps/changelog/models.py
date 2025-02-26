from django.contrib.postgres.fields import JSONField
from django.db import models

from apps.helpers.models import CreatedModel, UUIDModel, enum_max_length
from apps.project.models import Project


class ChangeLogActionType(models.TextChoices):
    CREATE = 'create', 'Создание'
    UPDATE = 'update', 'Изменение'
    DELETE = 'delete', 'Удаление'


class ChangeLogModelType(models.TextChoices):
    PROJECT = 'project', 'Проект'
    RMM_SETTINGS = 'rmm_settings', 'Настройки РММ'
    TERMINAL_SETTINGS = 'terminal_settings', 'Настройки терминала'
    PRODUCT = 'product', 'Продукт'


class ChangeLog(UUIDModel, CreatedModel):
    project = models.ForeignKey(Project, models.CASCADE, related_name='change_logs', null=True)
    model = models.CharField(
        verbose_name='Модель',
        choices=ChangeLogModelType.choices,
        max_length=enum_max_length(ChangeLogModelType),
    )
    record_id = models.UUIDField('ID измененной записи')
    action_on_model = models.CharField(
        verbose_name='Действие',
        choices=ChangeLogActionType.choices,
        max_length=enum_max_length(ChangeLogActionType),
    )
    changed_data = JSONField(verbose_name='Измененные данные модели')

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'Лог изменения модели'
        verbose_name_plural = 'Логи изменений моделей'
