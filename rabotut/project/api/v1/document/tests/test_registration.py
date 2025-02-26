import pytest

from apps.document.models import Registration
from apps.document.models.status.choices import BaseUserDocumentStatuses

pytestmark = [pytest.mark.django_db]


def test_create_registration(applicant_client, db_file):
    """Тест создания Страницы с регистрацией."""
    data = {'file': db_file.pk, 'registration_address': 'somewhere'}
    create_response = applicant_client.post('/api/v1/document/registration/', data=data)
    assert create_response.status_code == 200


def test_create_registration_by_admin(
    master_client,
    db_file,
    applicant_user,
):
    """Тест создания Страницы с регистрацией от админа для аппликанта."""
    data = {'file': db_file.pk, 'registration_address': 'somewhere', 'user': applicant_user.pk}
    master_client.post('/api/v1/document/registration/', data=data)
    registration = Registration.objects.first()
    assert registration.user.pk == applicant_user.pk


@pytest.mark.parametrize(
    'client_fixture, registration, document_status',
    [
        ('applicant_client', 'registration_status_decline', BaseUserDocumentStatuses.APPROVAL),
        ('master_client', 'registration_status_approval', BaseUserDocumentStatuses.APPROVAL),
        ('master_client', 'registration_status_accept', BaseUserDocumentStatuses.ACCEPT),
    ]
)
def test_patch_registration(
    client_fixture,
    registration,
    document_status,
    request,
    db_file,
):
    """Тест patch изменения страницы с регистрацией."""
    registration = request.getfixturevalue(registration)
    url = f'/api/v1/document/registration/{registration.id}/'
    update_registration_data = {
        'file': [db_file.id],
    }

    response = request.getfixturevalue(client_fixture).patch(path=url, data=update_registration_data)
    registration.refresh_from_db()

    assert response.status_code == 200
    assert registration.status == document_status


@pytest.mark.parametrize(
    'client_fixture, registration, document_status',
    [
        ('applicant_client', 'registration_status_decline', BaseUserDocumentStatuses.APPROVAL),
        ('master_client', 'registration_status_approval', BaseUserDocumentStatuses.APPROVAL),
        ('master_client', 'registration_status_accept', BaseUserDocumentStatuses.ACCEPT),
    ]
)
def test_put_registration(
    client_fixture,
    registration,
    document_status,
    request,
    db_file,
):
    """Тест put изменения страницы с регистрацией."""
    registration = request.getfixturevalue(registration)
    url = f'/api/v1/document/registration/{registration.id}/'
    update_registration_data = {
        'file': [db_file.id],
        'status': registration.status,
        'registration_address': 'г.Саранск',
        'user': registration.user.id,
    }

    response = request.getfixturevalue(client_fixture).put(path=url, data=update_registration_data)
    registration.refresh_from_db()

    assert response.status_code == 200
    assert registration.status == document_status
