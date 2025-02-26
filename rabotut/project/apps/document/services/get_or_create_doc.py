from typing import Dict, Union

from django.db.models import Model
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from apps.document.models import Inn, Passport, Registration, Selfie, Snils
from apps.document.models.status.choices import BaseUserDocumentStatuses
from apps.helpers.services import AbstractService


class GetOrCreateDocumentService(AbstractService):
    """Сервис создает новый документ или обновляет существующий (отправляет на перепроверку)."""

    def __init__(
        self,
        model: Union[Inn | Passport | Registration | Selfie | Snils],
        validated_data: Dict,
        serializer: ModelSerializer,
    ):
        self.model = model
        self.serializer = serializer
        self.validated_data = validated_data

    def process(self) -> Model:
        exist_docs = self.model.objects.filter(user=self.validated_data.get('user'))
        if not exist_docs.exists():
            return self._create_new_document()

        exist_doc = exist_docs.first()
        if self._check_exist_document(exist_doc):
            return exist_doc

        # Если документ у юзера уже есть - обновить новыми данными и отправить на перепроверку
        self.validated_data['status'] = BaseUserDocumentStatuses.APPROVAL
        self.validated_data['rejection_reason'] = None
        self.serializer.update(exist_doc, self.validated_data)
        return exist_doc

    def _create_new_document(self) -> Union[Inn | Passport | Registration | Selfie | Snils]:
        """Создание нового документа."""
        self.validated_data['status'] = BaseUserDocumentStatuses.APPROVAL
        if self.model == Registration:
            new_doc = self._make_registration_document()
        else:
            new_doc = self.model.objects.create(**self.validated_data)
        return new_doc

    def _make_registration_document(self) -> Registration:
        """Создание документа со страницей регистрации."""
        infile = self.validated_data.pop('file')
        new_doc = self.model.objects.create(**self.validated_data)
        new_doc.file.set(infile)
        new_doc.save()
        return new_doc

    def _check_exist_document(self, exist_doc: Union[Inn | Passport | Registration | Selfie | Snils]) -> bool:
        """Если есть такой документ, проверить что он того юзера, который делает запрос."""
        if exist_doc.user != self.validated_data.get('user'):
            raise ValidationError(f'Данный {self.model._meta.verbose_name} уже существует в системе.')  # noqa: WPS437
        # Обновить можно только документ со статусом Отклонен
        return exist_doc.status == BaseUserDocumentStatuses.DECLINE
