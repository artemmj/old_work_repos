import pytest

from apps.document.models import Selfie
from apps.document.models.status.choices import BaseUserDocumentStatuses

pytestmark = [pytest.mark.django_db]


def test_create_selfie(applicant_client, passport_fixture, db_file):
    """Тест создания Селфи."""
    data = {'file': db_file.pk}
    create_response = applicant_client.post('/api/v1/document/selfie/', data=data)
    assert create_response.status_code == 200


def test_create_selfie_by_admin(
    master_client,
    db_file,
    applicant_user,
    passport,
):
    """Тест создания Селфи от админа для аппликанта."""
    data = {'file': db_file.pk, 'user': applicant_user.pk}
    master_client.post('/api/v1/document/selfie/', data=data)
    selfie = Selfie.objects.first()
    assert selfie.user == applicant_user


@pytest.mark.parametrize(
    'client_fixture, selfie, document_status',
    [
        ('applicant_client', 'selfie_status_decline', BaseUserDocumentStatuses.APPROVAL),
        ('master_client', 'selfie_status_approval', BaseUserDocumentStatuses.APPROVAL),
        ('master_client', 'selfie_status_accept', BaseUserDocumentStatuses.ACCEPT),
    ]
)
def test_patch_selfie(
    client_fixture,
    selfie,
    document_status,
    request,
    db_file,
):
    """Тест patch изменения селфи."""
    selfie = request.getfixturevalue(selfie)
    url = f'/api/v1/document/selfie/{selfie.id}/'
    update_selfie_data = {
        'file': db_file.id,
    }

    response = request.getfixturevalue(client_fixture).patch(path=url, data=update_selfie_data)
    selfie.refresh_from_db()

    assert response.status_code == 200
    assert selfie.status == document_status


@pytest.mark.parametrize(
    'client_fixture, selfie, document_status',
    [
        ('applicant_client', 'selfie_status_decline', BaseUserDocumentStatuses.APPROVAL),
        ('master_client', 'selfie_status_approval', BaseUserDocumentStatuses.APPROVAL),
        ('master_client', 'selfie_status_accept', BaseUserDocumentStatuses.ACCEPT),
    ]
)
def test_put_selfie(
    client_fixture,
    selfie,
    document_status,
    request,
    db_file,
):
    """Тест put изменения селфи."""
    selfie = request.getfixturevalue(selfie)
    url = f'/api/v1/document/selfie/{selfie.id}/'
    update_selfie_data = {
        'file': db_file.id,
        'status': selfie.status,
        'user': selfie.user.id,
    }

    response = request.getfixturevalue(client_fixture).put(path=url, data=update_selfie_data)
    selfie.refresh_from_db()

    assert response.status_code == 200
    assert selfie.status == document_status
