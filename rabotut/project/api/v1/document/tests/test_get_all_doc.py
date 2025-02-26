import pytest


@pytest.mark.django_db
def test_get_all_doc(
    passport_fixture,
    snils_fixture,
    inn_fixture,
    registration_fixture,
    selfie_fixture,
    applicant_client,
    phone,
    api_v1_document_all,
):
    data = {'user_phone': phone}
    response = applicant_client.get(api_v1_document_all, data=data)
    assert response.status_code == 200
    assert response.json() is not None
