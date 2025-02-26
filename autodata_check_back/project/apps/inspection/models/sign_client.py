from django.db import models

from apps.file.models import Image
from apps.helpers.models import CreatedModel, UUIDModel
from apps.inspection.models.inspection import Inspection


class SignClient(UUIDModel, CreatedModel):
    image = models.ForeignKey(
        Image,
        verbose_name='Подпись клиента',
        related_name='signs_client',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    inspection = models.OneToOneField(
        Inspection,
        verbose_name='Осмотр',
        related_name='sign_client',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    accreditation_inspection = models.OneToOneField(
        'inspector_accreditation.AccreditationInspection',
        verbose_name='Осмотр на аккредитацию',
        related_name='sign_client',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Подпись клиента'
        verbose_name_plural = 'Подписи клиентов'
