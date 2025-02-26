from django.db import models

from apps.helpers.consts import CHAR_FIELD_MIDDLE_LENGTH
from apps.helpers.models import DefaultModel


class Department(DefaultModel):
    name = models.CharField('Название', max_length=CHAR_FIELD_MIDDLE_LENGTH)

    class Meta:
        verbose_name = 'Департамент'
        verbose_name_plural = 'Департаменты'

    def __str__(self):
        return self.name
