import base64
import dataclasses
import json
import logging
from datetime import datetime
from typing import Dict, Optional

import httpx
from django.conf import settings
from django.core.files.storage import default_storage
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from apps.file.models import File
from apps.helpers.services import AbstractService

log = logging.getLogger('django')


class PassportRecognitionError(ValidationError):
    """Документ не распознан или не поддерживается."""


@dataclasses.dataclass
class PassportRecognitionData:
    gender: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    patronymic: Optional[str] = None
    birth_date: Optional[str] = None
    citizenship: str = 'РФ'
    number: Optional[str] = None
    series: Optional[str] = None
    department_code: Optional[str] = None
    date_issue: Optional[str] = None
    issued_by: Optional[str] = None
    place_of_birth: Optional[str] = None

    def __iter__(self):
        return iter(dataclasses.astuple(self))


@dataclasses.dataclass
class PassportRecognitionResponse:
    recognized_data: PassportRecognitionData = dataclasses.field(default_factory=PassportRecognitionData)
    full_recognition: bool = False
    partial_recognition: bool = False
    success: bool = False
    error: str = ''


class PassportRecognitionService(AbstractService):
    """Сервис по распознаванию данных паспорта, обращается в сторонний сервис."""

    def __init__(self, passport_file: File):
        self.passport_file = passport_file
        self.headers = {
            'Auth': settings.PASSPORT_RECOGNITION_AUTH_TOKEN,
            'ClientId': settings.PASSPORT_RECOGNITION_CLIENT_ID,
            'Accept-Charset': 'utf-8',
            'Content-Type': 'application/json',
        }
        self.response: Optional[Response] = None

    def process(self) -> Dict:
        self.response = self._get_response().json()
        gender_map = {'МУЖ.': 'male', 'ЖЕН.': 'female'}

        return dataclasses.asdict(PassportRecognitionData(
            gender=gender_map.get(self._get_field('Gender')),
            first_name=self._get_field('Name'),
            last_name=self._get_field('Surname'),
            patronymic=self._get_field('Patronymic'),
            birth_date=self._to_datetime(self._get_field('BirthDate')),
            number=self._get_field('PassportNumber'),
            series=self._get_field('PassportSeries'),
            department_code=self._department_code(self._get_field('PassportAuthorityCode')),
            date_issue=self._to_datetime(self._get_field('PassportIssuedDate')),
            issued_by=self._get_field('PassportAuthority'),
            place_of_birth=self._get_field('BirthPlace'),
        ))

    def _get_response(self) -> Response:
        django_file = default_storage.open(str(self.passport_file.file.name)).read()
        payload = {
            'data': base64.b64encode(django_file).decode('utf-8'),
            'filename': self.passport_file.file.name.split('/')[-1],
            'isPaidRequest': False,
        }
        response = httpx.post(
            settings.PASSPORT_RECOGNITION_FULL_URL,
            headers=self.headers,
            data=json.dumps(payload),
            timeout=10,
        )
        self._validate_response(response)
        return response

    def _validate_response(self, response: Response) -> None:
        json_resp = response.json()
        if not json_resp.get('RecognizedDocumentFields'):
            details = json_resp.get('Details', None)
            raise PassportRecognitionError(f'Не удалось распознать. (details: {details})')

    def _get_field(self, field) -> str:
        try:
            return self.response['RecognizedDocumentFields'][field]['Value']
        except (KeyError, AttributeError):
            return None

    def _to_datetime(self, field: Optional[str]) -> Optional[str]:
        if not field:
            return field
        date_issue = datetime.strptime(field, '%d.%m.%Y')
        return datetime.strftime(date_issue, '%Y-%m-%d')

    def _department_code(self, field: Optional[str]) -> Optional[str]:
        if not field:
            return field
        return field.replace('-', '')
