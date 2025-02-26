import pytest

from apps.document.models import Inn
from apps.document.models.status.choices import BaseUserDocumentStatuses

pytestmark = [pytest.mark.django_db]


def test_create_inn(applicant_user, applicant_client, db_file):
    """Тест создания ИНН."""
    data = {'value': '153064444322', 'file': db_file.pk}
    create_response = applicant_client.post('/api/v1/document/inn/', data=data)
    assert create_response.status_code == 200
    inn = Inn.objects.first()
    assert inn.user == applicant_user


def test_fail_create_inn(applicant_client, db_file):
    """Тест неудачного создания ИНН с некорректным номером."""
    data = {'value': '15306444432', 'file': db_file.pk}
    fail_create_respone = applicant_client.post('/api/v1/document/inn/', data=data)
    assert fail_create_respone.status_code == 400


def test_create_inn_by_admin(master_user, master_client, db_file, applicant_user):
    """Тест создания ИНН от админа для аппликанта."""
    data = {'value': '153064444322', 'file': db_file.pk, 'user': applicant_user.pk}
    master_client.post('/api/v1/document/inn/', data=data)
    inn = Inn.objects.first()
    assert inn.user.pk == applicant_user.pk


@pytest.mark.parametrize(
    'client_fixture, inn, document_status',
    [
        ('applicant_client', 'inn_status_decline', BaseUserDocumentStatuses.APPROVAL),
        ('master_client', 'inn_status_approval', BaseUserDocumentStatuses.APPROVAL),
        ('master_client', 'inn_status_accept', BaseUserDocumentStatuses.ACCEPT),
    ]
)
def test_patch_inn(
    client_fixture,
    inn,
    document_status,
    request,
):
    """Тест patch изменения инн."""
    inn = request.getfixturevalue(inn)
    url = f'/api/v1/document/inn/{inn.id}/'
    update_inn_data = {
        'value': '231404313580',
    }

    response = request.getfixturevalue(client_fixture).patch(path=url, data=update_inn_data)
    inn.refresh_from_db()

    assert response.status_code == 200
    assert inn.status == document_status


@pytest.mark.parametrize(
    'client_fixture, inn, document_status',
    [
        ('applicant_client', 'inn_status_decline', BaseUserDocumentStatuses.APPROVAL),
        ('master_client', 'inn_status_approval', BaseUserDocumentStatuses.APPROVAL),
        ('master_client', 'inn_status_accept', BaseUserDocumentStatuses.ACCEPT),
    ]
)
def test_put_inn(
    client_fixture,
    inn,
    document_status,
    request,
    db_file,
):
    """Тест put изменения инн."""
    inn = request.getfixturevalue(inn)
    url = f'/api/v1/document/inn/{inn.id}/'
    update_inn_data = {
        'value': '231404313580',
        'verification_at': '2024-12-03T13:19:25.168Z',
        'is_self_employed': True,
        'is_manual_verification_required': True,
        'file': db_file.id,
        'status': inn.status,
        'user': inn.user.id,
    }

    response = request.getfixturevalue(client_fixture).put(path=url, data=update_inn_data)
    inn.refresh_from_db()

    assert response.status_code == 200
    assert inn.status == document_status
