from django.db import models

from apps.helpers.models import UUIDModel


class RMMSettings(UUIDModel):
    project = models.OneToOneField(
        'project.Project', verbose_name='Проект', related_name='rmm_settings', on_delete=models.CASCADE,
    )
    auto_zones_amount = models.PositiveSmallIntegerField('Кол-во автоназначаемых зон', default=0)
    password = models.CharField('Пароль для редактирования настроек', max_length=10, default='555')
    norm = models.PositiveSmallIntegerField('Норма счётчика', null=True, blank=True)
    extended_tasks = models.NullBooleanField('Расширенный механизм заданий', default=False)

    class Meta:
        verbose_name = 'Настройки параметров РММ'
        verbose_name_plural = 'Настройки параметров РММ'

    def __str__(self):
        return f'Настройки параметров РММ проекта {self.project.title}'
