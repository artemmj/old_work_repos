import pytest

from apps.document.models.status.choices import BaseUserDocumentStatuses
from apps.document.services.get_all_users_doc import DocumentsOfUserService


@pytest.mark.django_db
def test_process(applicant_user, passport_fixture, snils_fixture, inn_fixture, registration_fixture, selfie_fixture):
    result = DocumentsOfUserService().process(user=applicant_user)

    assert 'passport' in result
    assert 'inn' in result
    assert 'snils' in result
    assert 'registration' in result
    assert 'selfie' in result
    assert result['status'] == BaseUserDocumentStatuses.ACCEPT


@pytest.mark.django_db
def test_status_invalid(
    applicant_user,
    passport_fixture,
    snils_fixture,
    inn_fixture,
    registration_fixture,
    selfie_fixture,
):
    result = DocumentsOfUserService().process(user=applicant_user)
    assert result['status'] != BaseUserDocumentStatuses.DECLINE


@pytest.mark.django_db
def test_get_status_approval(
    applicant_user,
    passport_fixture,
    snils_fixture,
    inn_fixture,
    registration_fixture,
    selfie_fixture,
):
    passport_fixture.status = BaseUserDocumentStatuses.APPROVAL
    passport_fixture.save()
    result = DocumentsOfUserService().process(user=applicant_user)
    assert result['status'] == BaseUserDocumentStatuses.APPROVAL


@pytest.mark.django_db
def test_get_status_decline(
    applicant_user,
    passport_fixture,
    snils_fixture,
    inn_fixture,
    registration_fixture,
    selfie_fixture,
):
    passport_fixture.status = BaseUserDocumentStatuses.DECLINE
    passport_fixture.save()
    result = DocumentsOfUserService().process(user=applicant_user)
    assert result['status'] == BaseUserDocumentStatuses.DECLINE
