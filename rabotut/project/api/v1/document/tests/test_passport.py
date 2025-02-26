import pytest

from apps.document.models import Passport
from apps.document.models.status.choices import BaseUserDocumentStatuses

pytestmark = [pytest.mark.django_db]


def test_create_passport(applicant_client, passport_data):
    """Тест создания Паспортов."""
    create_response = applicant_client.post('/api/v1/document/passport/', data=passport_data)
    assert create_response.status_code == 200


def test_create_passport_by_admin(master_client, db_file, applicant_user, passport_data):
    """Тест создания Паспорта от админа для аппликанта."""
    passport_data['file'] = db_file.pk
    passport_data['user'] = applicant_user.pk
    master_client.post('/api/v1/document/passport/', data=passport_data)
    passport = Passport.objects.first()
    assert passport.user.pk == applicant_user.pk


@pytest.mark.parametrize(
    'client_fixture, passport, document_status',
    [
        ('applicant_client', 'passport_status_decline', BaseUserDocumentStatuses.APPROVAL),
        ('master_client', 'passport_status_approval', BaseUserDocumentStatuses.APPROVAL),
        ('master_client', 'passport_status_accept', BaseUserDocumentStatuses.ACCEPT),
    ]
)
def test_patch_passport(
    client_fixture,
    passport,
    document_status,
    request,
):
    """Тест patch изменения паспорта."""
    passport = request.getfixturevalue(passport)
    url = f'/api/v1/document/passport/{passport.id}/'
    update_passport_data = {
        'last_name': 'Александр',
    }
    response = request.getfixturevalue(client_fixture).patch(path=url, data=update_passport_data)
    passport.refresh_from_db()
    assert response.status_code == 200
    assert passport.status == document_status


@pytest.mark.parametrize(
    'client_fixture, passport, document_status',
    [
        ('applicant_client', 'passport_status_decline', BaseUserDocumentStatuses.APPROVAL),
        ('master_client', 'passport_status_approval', BaseUserDocumentStatuses.APPROVAL),
        ('master_client', 'passport_status_accept', BaseUserDocumentStatuses.ACCEPT),
    ]
)
def test_put_passport(
    client_fixture,
    passport,
    document_status,
    request,
    db_file,
):
    """Тест put изменения паспорта."""
    passport = request.getfixturevalue(passport)
    url = f'/api/v1/document/passport/{passport.id}/'
    update_passport_data = {
        'user': passport.user.id,
        'status': passport.status,
        'gender': 'male',
        'birth_date': '1982-09-12',
        'place_of_birth': 'Саранск',
        'citizenship': 'РФ',
        'number': '528070',
        'series': '5284',
        'department_code': '479225',
        'date_issue': '2004-12-17',
        'issued_by': 'Выдан',
        'first_name': 'Иван',
        'last_name': 'Иванов',
        'patronymic': 'Иванович',
        'file': db_file.id,
    }

    response = request.getfixturevalue(client_fixture).put(path=url, data=update_passport_data)
    passport.refresh_from_db()

    assert response.status_code == 200
    assert passport.status == document_status
