from django.db import models

from apps.helpers.models import CreatedModel, UUIDModel


class InspectionTaskSearch(UUIDModel, CreatedModel):
    task = models.OneToOneField(
        'inspection_task.InspectionTask',
        verbose_name='Задание на осмотр',
        related_name='inspection_task_search',
        on_delete=models.PROTECT,
    )
    level = models.PositiveSmallIntegerField('Уровень поиска', default=0)
    start_time = models.DateTimeField('Начало поиска', auto_now_add=True)
    start_time_iter = models.DateTimeField('Начало итерации поиска', auto_now_add=True)
    is_active = models.BooleanField('Активная', default=False)

    class Meta:
        verbose_name = 'Объект поиска инспекторов'
        verbose_name_plural = 'Объекты поиска инспекторов'
