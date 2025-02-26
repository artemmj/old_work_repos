from typing import Dict

from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.request import Request
from rest_framework.status import HTTP_404_NOT_FOUND

from apps.arketa.clients import ArketaServiceApiClient, ArketaTaskApiClient
from apps.document.models.status.choices import BaseUserDocumentStatuses
from apps.document.services import DocumentsOfUserService
from apps.helpers.services import AbstractService


class ValidateCheckDocumentService(AbstractService):
    """
    Сервис для проверки подтверждения доков в нашем беке и наличие юзера в аркете.

    Если есть проблема с документами работута - рейзим ошибку. Если ок,
    проверяем в аркете. Рейзим ошибку если пользователя в аркете нет.
    Если есть, вернуть на мк инфо о документах аркеты - дальше они сами
    решают что делать исходя из статусов доков.
    """

    def __init__(self, request: Request):
        self.request = request

    def process(self) -> Dict:
        self._check_rabotut_documents()
        self._check_user_arketa_exists()

        token = self.request.META.get('HTTP_AUTHORIZATION')
        # Вернуть результат по документам в аркете, если все остальное ок
        return ArketaTaskApiClient(token).check_arketa_documents()

    def _check_rabotut_documents(self):
        """Проверить документы работута в первую очередь."""
        user_documents = DocumentsOfUserService().process(self.request.user)
        doc_status = user_documents.get('status')
        if not doc_status or doc_status in {BaseUserDocumentStatuses.DECLINE, BaseUserDocumentStatuses.APPROVAL}:
            raise ValidationError('Не подтверждены все необходимые документы в Работут.')

    def _check_user_arketa_exists(self):
        """Проверить наличие юзера в аркете."""
        service_result = ArketaServiceApiClient().check_user_exists(phone=self.request.user.phone)
        if 'errors' in service_result and service_result.get('status_code') == HTTP_404_NOT_FOUND:
            raise NotFound('Пользователь отсутствует в аркете.')
