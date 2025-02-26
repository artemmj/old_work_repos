import logging
from dataclasses import asdict

from rest_framework.exceptions import ValidationError

from apps.document.models.passport.passport import Passport
from apps.document.models.selfie.selfie import Selfie, SelfieRecognition, SelfieStatuses
from apps.document.services.face_matching_recognition import FaceMatchingRecognition
from apps.helpers.services import AbstractService

logger = logging.getLogger('django')


class VerifySelfiePassportService(AbstractService):
    """Сервис делает запрос на соответствие фото паспорта и лица, записывает результат."""

    def __init__(self, selfie: Selfie) -> None:
        self.selfie = selfie

    def process(self) -> None:
        self.recogn_response = asdict(FaceMatchingRecognition(self.selfie.file).process())
        passport = self._validate_passport()
        status = self._get_status()
        match_confirmation = self._get_match_confirmation()
        SelfieRecognition.objects.update_or_create(
            passport=passport,
            selfie=self.selfie,
            defaults={
                'recognition_result': self.recogn_response,
                'status': status,
                'match_confirmation': match_confirmation,
            },
        )

    def _validate_passport(self) -> Passport:
        user_passports = Passport.objects.filter(user=self.selfie.user)
        if not user_passports:
            raise ValidationError('У пользователя нет паспорта')
        return user_passports.first()

    def _get_status(self) -> str:
        status = SelfieStatuses.RECOGNITION_FAILED
        if self.recogn_response.get('faces_is_equal'):
            status = SelfieStatuses.RECOGNITION_SUCCEEDED
        return status

    def _get_match_confirmation(self) -> bool:
        match_confirmation = False
        if self.recogn_response.get('faces_is_equal'):
            match_confirmation = True
        return match_confirmation
