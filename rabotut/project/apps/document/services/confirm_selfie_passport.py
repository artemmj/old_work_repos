from rest_framework.exceptions import ValidationError

from apps.document.models.passport.passport import Passport
from apps.document.models.selfie.selfie import Selfie, SelfieRecognition
from apps.helpers.services import AbstractService


class ConfirmSelfiePassportService(AbstractService):
    """Сервис подтверждает, что фото паспорта соответсвует селфи с паспортом."""

    def process(self, passport: Passport, selfie: Selfie) -> None:
        recognitions = SelfieRecognition.objects.filter(
            passport=passport,
            selfie=selfie,
        )
        if not recognitions.exists():
            raise ValidationError('Не найден SelfieRecognition для паспорта и селфи.')
        recognition = recognitions.first()
        recognition.match_confirmation = True
        recognition.save()
