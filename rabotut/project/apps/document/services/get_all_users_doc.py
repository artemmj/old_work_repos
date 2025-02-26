from typing import Dict

from django.db.models import QuerySet

from apps.document.models import Inn, Passport, Registration, Selfie, Snils
from apps.document.models.status.choices import BaseUserDocumentStatuses
from apps.helpers.services import AbstractService
from apps.user.models import User


class DocumentsOfUserService(AbstractService):
    """Получение документов пользователя."""

    def process(self, user: User) -> Dict:
        return {
            'passport': self.get_passport(user=user),
            'inn': self.get_inn(user=user),
            'snils': self.get_snils(user=user),
            'registration': self.get_registration(user=user),
            'selfie': self.get_selfie(user=user),
            'status': self.get_status(user=user),
        }

    def get_status(self, user: User) -> str:
        statuses = (
            self.get_passport(user=user).first().status if self.get_passport(user=user).exists() else '',
            self.get_inn(user=user).first().status if self.get_inn(user=user).exists() else '',
            self.get_snils(user=user).first().status if self.get_snils(user=user).exists() else '',
            self.get_registration(user=user).first().status if self.get_registration(user=user).exists() else '',
            self.get_selfie(user=user).first().status if self.get_selfie(user=user).exists() else '',
        )
        match statuses:
            case _ if BaseUserDocumentStatuses.DECLINE in statuses:
                return BaseUserDocumentStatuses.DECLINE
            case _ if BaseUserDocumentStatuses.APPROVAL in statuses:
                return BaseUserDocumentStatuses.APPROVAL
            case _ if set(statuses) == {BaseUserDocumentStatuses.ACCEPT}:
                return BaseUserDocumentStatuses.ACCEPT
        return None

    @staticmethod
    def get_passport(user: User) -> QuerySet:
        return Passport.objects.non_deleted().filter(user=user)

    @staticmethod
    def get_inn(user: User) -> QuerySet:
        return Inn.objects.non_deleted().filter(user=user)

    @staticmethod
    def get_snils(user: User) -> QuerySet:
        return Snils.objects.non_deleted().filter(user=user)

    @staticmethod
    def get_registration(user: User) -> QuerySet:
        return Registration.objects.non_deleted().filter(user=user)

    @staticmethod
    def get_selfie(user: User) -> QuerySet:
        return Selfie.objects.non_deleted().filter(user=user)
