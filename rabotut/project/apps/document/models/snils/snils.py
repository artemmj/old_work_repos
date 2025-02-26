from dirtyfields import DirtyFieldsMixin
from django.db import models
from django_lifecycle import LifecycleModelMixin, hook
from simple_history.models import HistoricalRecords

from apps.arketa.tasks import send_document_to_arketa_task
from apps.document.models.status.choices import BaseUserDocumentStatuses
from apps.helpers.consts import CHAR_FIELD_MIDDLE_LENGTH
from apps.helpers.models import DefaultModel, enum_max_length

from .validators import SNILS_VALIDATORS

SNILS_MAX_LENGTH = 11


class Snils(LifecycleModelMixin, DirtyFieldsMixin, DefaultModel):
    """СНИЛС."""

    value = models.CharField(  # noqa: WPS110
        'Значение',
        max_length=SNILS_MAX_LENGTH,
        validators=SNILS_VALIDATORS,
        unique=True,
    )
    status = models.CharField(
        'Статус',
        choices=BaseUserDocumentStatuses.choices,
        max_length=enum_max_length(BaseUserDocumentStatuses),
        default=BaseUserDocumentStatuses.APPROVAL,
    )
    file = models.ForeignKey(  # noqa: WPS110
        'file.File',
        verbose_name='Снилс',
        on_delete=models.PROTECT,
        related_name='snils_documents',
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        'user.User',
        on_delete=models.PROTECT,
        related_name='snils',
        db_index=True,
    )
    history = HistoricalRecords()
    rejection_reason = models.CharField(
        'Причина отклонения',
        max_length=CHAR_FIELD_MIDDLE_LENGTH,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'СНИЛС'
        verbose_name_plural = 'СНИЛС'

    @hook('after_update', when='status', has_changed=True)
    def create_update_in_arketa(self):
        from api.v1.document.serializers import SnilsReadSerializer  # noqa: WPS433
        serialized_data = SnilsReadSerializer(self).data
        serialized_data['document_status'] = serialized_data.pop('status')
        send_document_to_arketa_task.delay(model='Snils', user_id=self.user.pk, document_data=serialized_data)
