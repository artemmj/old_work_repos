from dirtyfields import DirtyFieldsMixin
from django.db import models
from django_lifecycle import LifecycleModelMixin, hook
from simple_history.models import HistoricalRecords

from apps.arketa.tasks import send_document_to_arketa_task
from apps.document.models.status.choices import BaseUserDocumentStatuses
from apps.helpers.consts import CHAR_FIELD_INN_LENGTH, CHAR_FIELD_MIDDLE_LENGTH
from apps.helpers.models import DefaultModel, enum_max_length

from .validators import INN_VALIDATORS


class Inn(LifecycleModelMixin, DirtyFieldsMixin, DefaultModel):
    value = models.CharField(  # noqa: WPS110
        'Значение',
        max_length=CHAR_FIELD_INN_LENGTH,
        unique=True,
        validators=INN_VALIDATORS,
    )
    verification_at = models.DateTimeField('Дата проверки на самозанятого', null=True, blank=True)
    is_self_employed = models.BooleanField('Является самозанятым или нет', null=True, blank=True)
    is_manual_verification_required = models.BooleanField('Требуется ручная проверка или нет', default=False)
    file = models.ForeignKey(  # noqa: WPS110
        'file.File',
        verbose_name='ИНН',
        on_delete=models.PROTECT,
        related_name='inn_documents',
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        'user.User',
        on_delete=models.PROTECT,
        related_name='inn',
        db_index=True,
    )
    status = models.CharField(
        'Статус',
        choices=BaseUserDocumentStatuses.choices,
        max_length=enum_max_length(BaseUserDocumentStatuses),
        default=BaseUserDocumentStatuses.APPROVAL,
    )
    history = HistoricalRecords()
    rejection_reason = models.CharField(
        'Причина отклонения',
        max_length=CHAR_FIELD_MIDDLE_LENGTH,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'ИНН'
        verbose_name_plural = 'ИНН'

    @hook('after_update', when='status', has_changed=True)
    def create_update_in_arketa(self):
        from api.v1.document.serializers import InnWriteSerializer  # noqa: WPS433
        serialized_data = InnWriteSerializer(self).data
        serialized_data['document_status'] = serialized_data.pop('status')
        send_document_to_arketa_task.delay(model='Inn', user_id=self.user.pk, document_data=serialized_data)
