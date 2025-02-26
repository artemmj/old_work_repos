from typing import Union

from rest_framework.exceptions import ValidationError

from apps.document.models import Inn, Passport, Snils
from apps.helpers.services import AbstractService
from apps.user.models import User


class ValidateRequestUserDocumentService(AbstractService):
    """Сервис проверяет, что данный документ того пользователя, который делает запрос. Иначе рейз ошибки."""

    def process(self, model: Union[Inn, Snils, Passport], value: str, request_user: User):  # noqa: WPS110
        if model in {Inn, Snils}:
            instance = model.objects.filter(value=value).first()
        elif model == Passport:
            instance = model.objects.filter(number=value).first()

        if instance:
            # Если док есть, но принадлежит тому же пользователю, который делает запрос, не валидировать
            if instance.user != request_user:
                raise ValidationError(f'Данный {model._meta.verbose_name} уже существует в системе.')  # noqa: WPS437
