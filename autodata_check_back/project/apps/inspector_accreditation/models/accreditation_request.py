from typing import Final

from django.db import models
from django_lifecycle import LifecycleModelMixin, hook

from apps.helpers.inn_validator import inn_validator
from apps.helpers.models import CreatedModel, UUIDModel
from apps.inspector_accreditation.models import AccreditationInspection
from apps.template.models import Template

FIO_MAX_LEN: Final = 63
INN_MAX_LEN: Final = 12
COMPANY_MAX_LEN: Final = 127


class InspectorAccreditationRequest(LifecycleModelMixin, UUIDModel, CreatedModel):
    user = models.ForeignKey(
        'user.User',
        verbose_name='Пользователь',
        related_name='accreditation_requests',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    inn = models.CharField('ИНН', validators=[inn_validator], max_length=INN_MAX_LEN)
    work_skills = models.PositiveSmallIntegerField('Опыт работы')
    company = models.CharField('Компания', max_length=COMPANY_MAX_LEN)
    city = models.ForeignKey(
        'address.City',
        verbose_name='Город',
        related_name='accreditation_requests',
        on_delete=models.PROTECT,
    )
    radius = models.PositiveIntegerField('Радиус в км, в котором Инспектор получает заказы')
    availability_thickness_gauge = models.BooleanField(verbose_name='Наличие толщиномера')
    accreditation_inspection = models.ForeignKey(
        AccreditationInspection,
        verbose_name='Задание на осмотр',
        related_name='accreditation_requests',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Заявка на аккредитацию в инспектора'
        verbose_name_plural = 'Заявки на аккредитацию в инспекторов'

    def __str__(self):
        return f'{self.user} {self.company} {self.city}'

    @hook('after_create')
    def set_accreditation_inspection(self):
        accreditation_inspection = AccreditationInspection.objects.create(
            template=Template.objects.filter(is_accreditation=True).first(),
        )
        self.accreditation_inspection = accreditation_inspection  # noqa: WPS601
        self.save()
