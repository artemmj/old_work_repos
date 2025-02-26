from django.contrib.auth import get_user_model
from django.db import models
from django_lifecycle import LifecycleModel, hook

from apps.helpers.models import CreatedModel, UUIDModel
from apps.project.models.rmm_settings import RMMSettings
from apps.project.models.terminal_settings import TerminalSettings
from apps.template.models import Template, TemplateExport

User = get_user_model()


class Project(LifecycleModel, UUIDModel, CreatedModel):
    title = models.CharField('Название', max_length=200)
    address = models.CharField('Адрес', max_length=200)
    manager = models.ForeignKey(
        User,
        verbose_name='Менеджер',
        related_name='manager_projects',
        on_delete=models.PROTECT,
    )
    template = models.ForeignKey(
        Template,
        verbose_name='Шаблон',
        related_name='projects',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    template_export = models.ForeignKey(
        TemplateExport,
        verbose_name='Шаблон выгрузки',
        related_name='projects',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    accounting_without_yk = models.BooleanField('Учет без УК', default=False)
    auto_assign_enbale = models.BooleanField('Включено автоназначение задач для Скан', default=False)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return self.title

    @hook('after_create')
    def create_project_settings(self):
        RMMSettings.objects.create(project=self)
        TerminalSettings.objects.create(project=self)
