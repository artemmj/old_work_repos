from django.db import models
from django_lifecycle import LifecycleModel, hook

from apps.helpers.models import CreatedModel, enum_max_length
from apps.project.models import Project


class TitleChoices(models.TextChoices):
    FOR_THE_CLIENT = 'for_the_client', 'Для заказчика'
    PRODUCTS_CATALOG_LOAD = 'products_catalog_load', 'Загружен справочник/каталог'
    PRODUCTS_CATALOG_DELETE = 'products_catalog_delete', 'Удален справочник/каталог'
    TEMPLATE_DELETE = 'template_delete', 'Удален шаблон'
    ZONES_DELETE = 'zones_delete', 'Удалены зоны'
    CREATE_NEW_PROJECT = 'create_new_project', 'Создан новый проект'
    PROJECT_SETTINGS_LOAD = 'project_settings_load', 'Загружены настройки проекта'
    PROJECT_SETTINGS_UPDATE = 'project_settings_update', 'Обновлены настройки проекта'
    TERMINAL_SETTINGS_UPDATE = 'terminal_settings_update', 'Обновлены настройки терминала'
    RMM_SETTINGS_UPDATE = 'rmm_settings_update', 'Обновлены настройки РММ'
    EMPLOYEES_DELETE = 'employees_delete', 'Удалены пользователи'
    TERMINAL_LOAD_START = 'terminal_load_start', 'Запущен процесс загрузки терминалов'
    EXCLUDE_ZONE_FROM_AUTOASSIGNMENT = 'exclude_zone_from_autoassignment', 'Исключена зона из автоназначения'
    DOCUMENT_CHANGE_STATUS = 'document_change_status', 'Изменен статус документа'
    DOCUMENT_SPECIFICATION_EDITING = 'document_specification_editing', 'Измненение спецификации документа'
    EXPORT_PROJECT_DATA = 'export_project_data', 'Выгрузка данных проекта'
    EXPORT_TEMPLATE = 'export_template', 'Выгрузка шаблона'
    CHANGE_TEMPLATE = 'change_template', 'Изменен шаблон'
    UPDATE_ARTICLES = 'update_articles', 'Обновление артикулов'
    UPDATE_REMAINDER = 'update_remainder', 'Обновление остатка'
    IMPORT_PROJECT = 'import_project', 'Импорт проекта'
    READY_TERMINAL_DB = 'ready_terminal_db', 'Подготовка терминальной БД'


class Event(CreatedModel, LifecycleModel):
    fake_id = models.IntegerField(default=1)
    project = models.ForeignKey(Project, models.CASCADE, related_name='events', null=True, blank=True)
    title = models.CharField(
        verbose_name='Название события',
        max_length=enum_max_length(TitleChoices),
        choices=TitleChoices.choices,
        default=TitleChoices.FOR_THE_CLIENT,
    )
    comment = models.TextField('Комментарий к событию')

    class Meta:
        ordering = ('id',)
        verbose_name = 'Журнал событий'
        verbose_name_plural = 'Журнал событий'

    def __str__(self):
        return self.title

    @hook('after_create')
    def generate_fake_id(self):
        if last_event := Event.objects.filter(  # noqa: WPS337 WPS332
            project=self.project,
        ).exclude(
            pk=self.pk,
        ).order_by(
            'fake_id',
        ).last():
            self.fake_id = last_event.fake_id + 1  # noqa: WPS601
            self.save()
