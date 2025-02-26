from django.db import models
from django_lifecycle import LifecycleModelMixin, hook
from simple_history.models import HistoricalRecords

from apps.arketa.tasks import send_document_to_arketa_task
from apps.document.models.status.choices import BaseUserDocumentStatuses
from apps.helpers.consts import CHAR_FIELD_MIDDLE_LENGTH
from apps.helpers.models import DefaultModel, enum_max_length


class SelfieStatuses(models.TextChoices):
    RECOGNITION_SUCCEEDED = 'recognition_succeeded', 'Успешная автоматическая проверка'
    RECOGNITION_FAILED = 'recognition_failed', 'Ошибка автоматическай проверки'


class Selfie(LifecycleModelMixin, DefaultModel):
    file = models.ForeignKey(  # noqa: WPS110
        'file.File',
        verbose_name='файл селфи',
        on_delete=models.PROTECT,
        related_name='selfie_documents',
    )
    user = models.ForeignKey(
        'user.User',
        on_delete=models.PROTECT,
        related_name='selfie',
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
        ordering = ('-created_at',)
        verbose_name = 'селфи с паспортом'
        verbose_name_plural = 'селфи с паспортом'

    @hook('after_update', when='status', has_changed=True)
    def create_update_in_arketa(self):
        from api.v1.document.serializers import SelfieWriteSerializer  # noqa: WPS433
        serialized_data = SelfieWriteSerializer(self).data
        serialized_data['document_status'] = serialized_data.pop('status')
        send_document_to_arketa_task.delay(model='Selfie', user_id=self.user.pk, document_data=serialized_data)


class SelfieRecognition(DefaultModel):
    passport = models.ForeignKey(
        'document.Passport',
        verbose_name='паспорт',
        on_delete=models.PROTECT,
        related_name='selfie_recognitions',
    )
    selfie = models.ForeignKey(
        'document.Selfie',
        verbose_name='документ',
        on_delete=models.PROTECT,
        related_name='recognitions',
    )

    recognition_result = models.JSONField(default=dict, blank=True)
    status = models.CharField(
        'статус селфи',
        choices=SelfieStatuses.choices,
        max_length=enum_max_length(SelfieStatuses),
    )
    match_confirmation = models.BooleanField(
        'Подтверждение соответствия селфи с паспортом',
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'результат проверки селфи'
        verbose_name_plural = 'результаты проверки селфи'
