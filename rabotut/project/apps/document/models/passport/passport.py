from django.db import models
from django_lifecycle import LifecycleModelMixin, hook
from simple_history.models import HistoricalRecords

from apps.arketa.tasks import send_document_to_arketa_task
from apps.document.models.status.choices import BaseUserDocumentStatuses
from apps.helpers.consts import CHAR_FIELD_MIDDLE_LENGTH
from apps.helpers.models import DefaultModel, enum_max_length

from .validators import PASSPORT_DEPARTMENT_CODE_VALIDATORS, PASSPORT_NUMBER_VALIDATORS, PASSPORT_SERIES_VALIDATORS

CHAR_FIELD_LENGTH_40 = 40


class PassportGender(models.TextChoices):
    MALE = 'male', 'Мужской'
    FEMALE = 'female', 'Женский'


class Passport(LifecycleModelMixin, DefaultModel):
    gender = models.CharField(
        'Пол',
        choices=PassportGender.choices,
        max_length=enum_max_length(PassportGender),
    )
    birth_date = models.DateField('Дата рождения')
    place_of_birth = models.TextField('Место рождения')
    citizenship = models.CharField('Гражданство', max_length=CHAR_FIELD_LENGTH_40)
    number = models.CharField(
        'Номер',
        validators=PASSPORT_NUMBER_VALIDATORS,
        max_length=6,
        unique=True,
    )
    series = models.CharField('Серия', validators=PASSPORT_SERIES_VALIDATORS, max_length=4)
    department_code = models.CharField(
        'Код подразделения',
        validators=PASSPORT_DEPARTMENT_CODE_VALIDATORS,
        max_length=6,
    )
    date_issue = models.DateField('Дата выдачи')
    issued_by = models.TextField('Кем выдан')
    file = models.ForeignKey(  # noqa: WPS110
        'file.File',
        verbose_name='Паспорт',
        on_delete=models.PROTECT,
        related_name='passport_documents',
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        'user.User',
        on_delete=models.PROTECT,
        related_name='passport',
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
    first_name = models.CharField('Имя', max_length=CHAR_FIELD_MIDDLE_LENGTH)
    last_name = models.CharField('Фамилия', max_length=CHAR_FIELD_MIDDLE_LENGTH)
    patronymic = models.CharField('Отчество', max_length=CHAR_FIELD_MIDDLE_LENGTH)

    class Meta:
        verbose_name = 'Паспорт'
        verbose_name_plural = 'Паспорта'

    @hook('after_update', when='status', has_changed=True)
    def create_update_in_arketa(self):
        from api.v1.document.serializers import PassportReadSerializer  # noqa: WPS433
        serialized_data = PassportReadSerializer(self).data
        serialized_data['document_status'] = serialized_data.pop('status')
        serialized_data['citizenship'] = 'Российская Федерация'
        send_document_to_arketa_task.delay(model='Passport', user_id=self.user.pk, document_data=serialized_data)

    @hook('after_update', when='status', has_changed=True, is_now=BaseUserDocumentStatuses.ACCEPT)
    def assign_user_fio(self):
        from apps.document.services import AssigningFioUserService  # noqa: WPS433
        AssigningFioUserService(passport=self, user=self.user).process()
