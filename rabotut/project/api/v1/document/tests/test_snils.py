import pytest

from apps.document.models import Snils
from apps.document.models.status.choices import BaseUserDocumentStatuses

pytestmark = [pytest.mark.django_db]


def test_create_snils(applicant_client, db_file):
    """Тест создания СНИЛС."""
    data = {'file': db_file.pk, 'value': '12849881814'}
    create_response = applicant_client.post('/api/v1/document/snils/', data=data)
    assert create_response.status_code == 200


def test_fail_create_snils(applicant_client, db_file):
    """Тест неудачного создания СНИЛС с некорректным номером."""
    data = {'file': db_file.pk, 'value': '128498818141'}
    fail_respone = applicant_client.post('/api/v1/document/snils/', data=data)
    assert fail_respone.status_code == 400


def test_create_snils_by_admin(
    master_client,
    db_file,
    applicant_user,
):
    """Тест создания СНИЛС от админа для аппликанта."""
    data = {'file': db_file.pk, 'value': '12849881814', 'user': applicant_user.pk}
    master_client.post('/api/v1/document/snils/', data=data)
    snils = Snils.objects.first()
    assert snils.user.pk == applicant_user.pk


@pytest.mark.parametrize(
    'client_fixture, snils, document_status',
    [
        ('applicant_client', 'snils_status_decline', BaseUserDocumentStatuses.APPROVAL),
        ('master_client', 'snils_status_approval', BaseUserDocumentStatuses.APPROVAL),
        ('master_client', 'snils_status_accept', BaseUserDocumentStatuses.ACCEPT),
    ]
)
def test_patch_snils(
    client_fixture,
    snils,
    document_status,
    request,
):
    """Тест patch изменения снилс."""
    snils = request.getfixturevalue(snils)
    url = f'/api/v1/document/snils/{snils.id}/'
    update_snils_data = {
        'value': '15267513870',
    }

    response = request.getfixturevalue(client_fixture).patch(path=url, data=update_snils_data)
    snils.refresh_from_db()

    assert response.status_code == 200
    assert snils.status == document_status


@pytest.mark.parametrize(
    'client_fixture, snils, document_status',
    [
        ('applicant_client', 'snils_status_decline', BaseUserDocumentStatuses.APPROVAL),
        ('master_client', 'snils_status_approval', BaseUserDocumentStatuses.APPROVAL),
        ('master_client', 'snils_status_accept', BaseUserDocumentStatuses.ACCEPT),
    ]
)
def test_put_snils(
    client_fixture,
    snils,
    document_status,
    request,
    db_file,
):
    """Тест put изменения снилс."""
    snils = request.getfixturevalue(snils)
    url = f'/api/v1/document/snils/{snils.id}/'
    update_snils_data = {
        'value': '15267513870',
        'file': db_file.id,
        'user': snils.user.id,
    }

    response = request.getfixturevalue(client_fixture).put(path=url, data=update_snils_data)
    snils.refresh_from_db()

    assert response.status_code == 200
    assert snils.status == document_status
