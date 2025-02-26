from urllib.parse import urljoin

import httpx
import pytest
from django.conf import settings
from mixer.backend.django import mixer

from apps.document.models.status.choices import BaseUserDocumentStatuses


@pytest.fixture
def api_v1_document_all(phone):
    return '/api/v1/document/all/'


@pytest.fixture
def passport_fixture(applicant_user):
    return mixer.blend('document.Passport', user=applicant_user, status=BaseUserDocumentStatuses.ACCEPT)


@pytest.fixture
def snils_fixture(applicant_user):
    return mixer.blend('document.Snils', user=applicant_user, status=BaseUserDocumentStatuses.ACCEPT)


@pytest.fixture
def inn_fixture(applicant_user):
    return mixer.blend('document.Inn', user=applicant_user, status=BaseUserDocumentStatuses.ACCEPT)


@pytest.fixture
def registration_fixture(applicant_user):
    return mixer.blend('document.Registration', user=applicant_user, status=BaseUserDocumentStatuses.ACCEPT)


@pytest.fixture
def selfie_fixture(applicant_user):
    return mixer.blend('document.Selfie', user=applicant_user, status=BaseUserDocumentStatuses.ACCEPT)


@pytest.fixture
def passport_data(db_file):
    """Фикстура с данными для Паспорта."""
    return {
        'gender': 'male',
        'first_name': 'Евгений',
        'last_name': 'Имярек',
        'patronymic': 'Александрович',
        'birth_date': '1982-09-12',
        'citizenship': 'Российская Федерация',
        'number': '000000',
        'series': '1104',
        'department_code': '292000',
        'date_issue': '2004-12-17',
        'issued_by': 'ОТДЕЛОМ ВНУТРЕННИХ ДЕЛ ОКТЯБРЬСКОГО ОКРУГА ГОРОДА АРХАНГЕЛЬСКА',
        'place_of_birth': 'ГОР. АРХАНГЕЛЬСК',
        'file': db_file.pk,
    }


@pytest.fixture
def mock_success_face_recognition(respx_mock):
    """Мок успешного ответа апи Face Recognition."""
    response = httpx.Response(
        200,
        json={
            'faces_is_detected': True,
            'faces_is_equal': True,
            'probability': 'средняя',
            'probability_value': 0.47,
            'result': True,
        },
    )
    respx_mock.post(urljoin(settings.FACE_RECOGNITION_DOMAIN, 'verify')).mock(return_value=response)


@pytest.fixture
def mock_fail_face_recognition(respx_mock):
    """Мок неуспешного ответа апи Face Recognition."""
    response = httpx.Response(
        200,
        json={
            'faces_is_detected': False,
            'faces_is_equal': False,
            'probability': '',
            'probability_value': 0,
            'result': False,
            'error': 'Error',
        },
    )
    respx_mock.post(urljoin(settings.FACE_RECOGNITION_DOMAIN, 'verify')).mock(return_value=response)


@pytest.fixture
def mock_success_passport_recognition(respx_mock):
    """Мок успешного ответа апи распознавания паспорта."""
    response = httpx.Response(
        200,
        json={
            'RecognizedDocumentFields': {
                'PassportAuthority': {
                    'Name': 'authority',
                    'DocumentFieldType': 3,
                    'Value': 'ОУФМС РОССИИ ПО КРАСНОДАРСКОМУ КРАЮ В УСТЬ-ЛАБИНСКОМ РАЙОНЕ',
                    'IsAccepted': True,
                },
                'PassportAuthorityCode': {
                    'Name': 'authority_code',
                    'DocumentFieldType': 4,
                    'Value': '230-055',
                    'IsAccepted': True,
                },
                'BirthDate': {
                    'Name': 'birthdate',
                    'DocumentFieldType': 8,
                    'Value': '01.01.1995',
                    'IsAccepted': True,
                },
                'BirthPlace': {
                    'Name': 'birthplace',
                    'DocumentFieldType': 9,
                    'Value': 'ГОР. УСТЬ-ЛАБИНСК КРАСНОДАРСКОГО КРАЯ',
                    'IsAccepted': True,
                },
                'Gender': {
                    'Name': 'gender',
                    'DocumentFieldType': 13,
                    'Value': 'МУЖ.',
                    'IsAccepted': True,
                },
                'PassportIssuedDate': {
                    'Name': 'issue_date',
                    'DocumentFieldType': 2,
                    'Value': '01.10.2015',
                    'IsAccepted': True,
                },
                'Name': {
                    'Name': 'name',
                    'DocumentFieldType': 6,
                    'Value': 'Влас',
                    'IsAccepted': True,
                },
                'PassportNumber': {
                    'Name': 'number',
                    'DocumentFieldType': 1,
                    'Value': '784933',
                    'IsAccepted': True,
                },
                'Patronymic': {
                    'Name': 'patronymic',
                    'DocumentFieldType': 7,
                    'Value': 'Евгеньевич',
                    'IsAccepted': True,
                },
                'PassportSeries': {
                    'Name': 'series',
                    'DocumentFieldType': 0,
                    'Value': '0307',
                    'IsAccepted': True,
                },
                'Surname': {
                    'Name': 'surname',
                    'DocumentFieldType': 5,
                    'Value': 'Кутузов',
                    'IsAccepted': True,
                },
            },
        },
    )
    respx_mock.post(settings.PASSPORT_RECOGNITION_FULL_URL).mock(return_value=response)


@pytest.fixture
def mock_fail_passport_recognition(respx_mock):
    """Мок неуспешного ответа апи распознавания паспорта."""
    response = httpx.Response(
        200,
        json={
            'Details': 'Document type was not recognized or is not supported',
        },
    )
    respx_mock.post(settings.PASSPORT_RECOGNITION_FULL_URL).mock(return_value=response)
