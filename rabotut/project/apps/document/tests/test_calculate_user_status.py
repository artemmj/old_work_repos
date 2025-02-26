import pytest

from apps.document.services.calculate_user_status import CalculateUserStatusService
from apps.user.models.doc_statuses import UserDocStatuses


@pytest.mark.parametrize(
    'client, inn, passport, registration, selfie, snils, doc_status',
    [
        (
            'applicant_client',
            'inn_status_accept',
            'passport_status_accept',
            'registration_status_accept',
            'selfie_status_accept',
            'snils_status_accept',
            UserDocStatuses.ACCEPT,
        ),
        (
            'applicant_client',
            'inn_status_approval',
            'passport_status_approval',
            'registration_status_approval',
            'selfie_status_approval',
            'snils_status_approval',
            UserDocStatuses.APPROVAL,
        ),
        (
            'applicant_client',
            'inn_status_approval',
            'passport_status_accept',
            'registration_status_accept',
            'selfie_status_accept',
            'snils_status_decline',
            UserDocStatuses.DECLINE,
        ),
    ]
)
@pytest.mark.django_db
def test_calculate_user_accept_status_service(client, request, inn, passport, registration, selfie, snils, doc_status):
    client = request.getfixturevalue(client)
    inn = request.getfixturevalue(inn)
    passport = request.getfixturevalue(passport)
    registration = request.getfixturevalue(registration)
    selfie = request.getfixturevalue(selfie)
    snils = request.getfixturevalue(snils)
    CalculateUserStatusService(inn).process()

    assert inn.user.doc_status == doc_status
