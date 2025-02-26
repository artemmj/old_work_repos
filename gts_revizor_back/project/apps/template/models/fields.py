from django.db import models

from apps.helpers.models import UUIDModel


class TemplateField(UUIDModel):
    name = models.CharField('Название', max_length=200)
    value = models.CharField('Значение', max_length=200)
    is_reusable = models.BooleanField(
        'Многоразовое?',
        help_text='Можно ли данное поле использовать несколько раз',
        default=False,
        db_index=True,
    )

    class Meta:
        ordering = ('name', )
        verbose_name = 'Поле шаблона'
        verbose_name_plural = 'Поля шаблона'

    def __str__(self):
        return self.name
