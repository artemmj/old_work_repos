import pytest
from mixer.auto import mixer

from apps.document.models import Inn, Passport, Registration, Selfie, Snils
from apps.document.models.status.choices import BaseUserDocumentStatuses


@pytest.fixture
def api_v1_document_all(phone):
    return '/api/v1/document/all/'


@pytest.fixture
def passport(applicant_user):
    return mixer.blend(Passport, user=applicant_user, status=BaseUserDocumentStatuses.ACCEPT)


@pytest.fixture
def snils(applicant_user):
    return mixer.blend(Snils, user=applicant_user, status=BaseUserDocumentStatuses.ACCEPT)


@pytest.fixture
def inn(applicant_user):
    return mixer.blend(Inn, user=applicant_user, status=BaseUserDocumentStatuses.ACCEPT)


@pytest.fixture
def registration(applicant_user):
    return mixer.blend(Registration, user=applicant_user, status=BaseUserDocumentStatuses.ACCEPT)


@pytest.fixture
def selfie(applicant_user):
    return mixer.blend(Selfie, user=applicant_user, status=BaseUserDocumentStatuses.ACCEPT)
