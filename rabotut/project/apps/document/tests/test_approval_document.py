import pytest

from apps.document.models.status.choices import BaseUserDocumentStatuses
from apps.document.services import ApprovalDocumentService

pytestmark = [pytest.mark.django_db]


@pytest.mark.parametrize(
    'user_fixture, passport, document_status',
    [
        ('applicant_user', 'passport_status_decline', BaseUserDocumentStatuses.APPROVAL),
        ('master_user', 'passport_status_approval', BaseUserDocumentStatuses.APPROVAL),
        ('master_user', 'passport_status_accept', BaseUserDocumentStatuses.ACCEPT),
    ]
)
def test_approval_passport(
    user_fixture,
    passport,
    document_status,
    request,
):
    """Тест перевода паспорта в статус проверка, при условии, что у пользователя роль не Мастер."""
    passport = request.getfixturevalue(passport)

    ApprovalDocumentService(
        document=passport,
        user_role=request.getfixturevalue(user_fixture).role,
    ).process()

    assert passport.status == document_status


@pytest.mark.parametrize(
    'user_fixture, inn, document_status',
    [
        ('applicant_user', 'inn_status_decline', BaseUserDocumentStatuses.APPROVAL),
        ('master_user', 'inn_status_approval', BaseUserDocumentStatuses.APPROVAL),
        ('master_user', 'inn_status_accept', BaseUserDocumentStatuses.ACCEPT),
    ]
)
def test_approval_inn(
    user_fixture,
    inn,
    document_status,
    request,
):
    """Тест перевода ИНН в статус проверка, при условии, что у пользователя роль не Мастер."""
    inn = request.getfixturevalue(inn)

    ApprovalDocumentService(
        document=inn,
        user_role=request.getfixturevalue(user_fixture).role,
    ).process()

    assert inn.status == document_status


@pytest.mark.parametrize(
    'user_fixture, registration, document_status',
    [
        ('applicant_user', 'registration_status_decline', BaseUserDocumentStatuses.APPROVAL),
        ('master_user', 'registration_status_approval', BaseUserDocumentStatuses.APPROVAL),
        ('master_user', 'registration_status_accept', BaseUserDocumentStatuses.ACCEPT),
    ]
)
def test_approval_registration(
    user_fixture,
    registration,
    document_status,
    request,
):
    """Тест перевода страницы с регистрацией в статус проверка, при условии, что у пользователя роль не Мастер."""
    registration = request.getfixturevalue(registration)

    ApprovalDocumentService(
        document=registration,
        user_role=request.getfixturevalue(user_fixture).role,
    ).process()

    assert registration.status == document_status


@pytest.mark.parametrize(
    'user_fixture, selfie, document_status',
    [
        ('applicant_user', 'selfie_status_decline', BaseUserDocumentStatuses.APPROVAL),
        ('master_user', 'selfie_status_approval', BaseUserDocumentStatuses.APPROVAL),
        ('master_user', 'selfie_status_accept', BaseUserDocumentStatuses.ACCEPT),
    ]
)
def test_approval_selfie(
    user_fixture,
    selfie,
    document_status,
    request,
):
    """Тест перевода селфи в статус проверка, при условии, что у пользователя роль не Мастер."""
    selfie = request.getfixturevalue(selfie)

    ApprovalDocumentService(
        document=selfie,
        user_role=request.getfixturevalue(user_fixture).role,
    ).process()

    assert selfie.status == document_status


@pytest.mark.parametrize(
    'user_fixture, snils, document_status',
    [
        ('applicant_user', 'snils_status_decline', BaseUserDocumentStatuses.APPROVAL),
        ('master_user', 'snils_status_approval', BaseUserDocumentStatuses.APPROVAL),
        ('master_user', 'snils_status_accept', BaseUserDocumentStatuses.ACCEPT),
    ]
)
def test_approval_snils(
    user_fixture,
    snils,
    document_status,
    request,
):
    """Тест перевода снилс в статус проверка, при условии, что у пользователя роль не Мастер."""
    snils = request.getfixturevalue(snils)

    ApprovalDocumentService(
        document=snils,
        user_role=request.getfixturevalue(user_fixture).role,
    ).process()

    assert snils.status == document_status
