from typing import Final

from django.db import models
from django_lifecycle import LifecycleModelMixin

from apps.helpers.inn_validator import inn_validator
from apps.helpers.models import CreatedModel, UUIDModel

_FIELD_MAX_LENGTH: Final = 40


class TypeInspectorChoices(models.TextChoices):
    LEGAL = 'legal', 'Юридическое лицо'   # noqa: WPS115
    INDIVIDUAL = 'individual', 'Индивидуальный предприниматель'   # noqa: WPS115


class Inspector(LifecycleModelMixin, UUIDModel, CreatedModel):
    inn = models.CharField(
        'ИНН',
        validators=[inn_validator],
        max_length=12,    # noqa: WPS432
        default='',
        null=True,
        blank=True,
    )
    work_skills = models.CharField('Опыт работы', max_length=1000, default='', null=True, blank=True)
    availability_thickness_gauge = models.BooleanField(
        verbose_name='Наличие толщиномера',
        default=True,
    )
    city = models.ForeignKey(
        'address.City',
        verbose_name='Город',
        related_name='inspectors',
        on_delete=models.PROTECT,
    )
    radius = models.PositiveIntegerField(
        'Радиус в км, в котором Инспектор получает заказы',
        default=0,
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        'user.User',
        verbose_name='Пользователь',
        related_name='inspectors',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    balance = models.DecimalField('Баланс', max_digits=19, decimal_places=2, default=0)   # noqa: WPS432

    class Meta:
        verbose_name = 'Инспектор'
        verbose_name_plural = 'Инспекторы'

    def __str__(self):
        return f'{self.user.last_name} {self.user.first_name}'   # noqa: WPS237
