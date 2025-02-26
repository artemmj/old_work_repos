from django.db import models
from django_lifecycle import LifecycleModelMixin, hook
from simple_history.models import HistoricalRecords

from apps.arketa.tasks import send_document_to_arketa_task
from apps.document.models.status.choices import BaseUserDocumentStatuses
from apps.helpers.consts import CHAR_FIELD_MIDDLE_LENGTH
from apps.helpers.models import DefaultModel, enum_max_length


class Registration(LifecycleModelMixin, DefaultModel):
    file = models.ManyToManyField(  # noqa: WPS110
        'file.File',
        verbose_name='Страницы с регистрацией',
        related_name='registration_documents',
    )
    status = models.CharField(
        'Статус',
        choices=BaseUserDocumentStatuses.choices,
        max_length=enum_max_length(BaseUserDocumentStatuses),
        default=BaseUserDocumentStatuses.APPROVAL,
    )
    registration_address = models.TextField('Адрес регистрации')
    user = models.ForeignKey(
        'user.User',
        on_delete=models.PROTECT,
        related_name='registration',
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
        verbose_name = 'страница с регистрацией'
        verbose_name_plural = 'страницы с регистрацией'

    @hook('after_update', when='status', has_changed=True)
    def create_update_in_arketa(self):
        from api.v1.document.serializers import RegistrationWriteSerializer  # noqa: WPS433
        serialized_data = RegistrationWriteSerializer(self).data
        serialized_data['document_status'] = serialized_data.pop('status')
        send_document_to_arketa_task.delay(model='Registration', user_id=self.user.pk, document_data=serialized_data)
