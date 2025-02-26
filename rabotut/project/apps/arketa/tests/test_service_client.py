import pytest

from apps.arketa.clients import ArketaServiceApiClient



@pytest.mark.django_db
def test_api_client_create_user(mock_201_arketa_create_user, inn_status_accept, applicant_user):
    result = ArketaServiceApiClient().create_user(applicant_user)
    assert result.get('results')


@pytest.mark.django_db
def test_fail_400_api_client_create_user(mock_400_arketa_create_user, inn_status_accept, applicant_user):
    result = ArketaServiceApiClient().create_user(applicant_user)
    assert not result.get('results')


@pytest.mark.django_db
def test_fail_500_service_api_client_create_user(
    mock_500_arketa_service_api_client_create_user,
    inn_status_accept,
    applicant_user,
):
    result = ArketaServiceApiClient().create_user(applicant_user)
    assert not result.get('results')


@pytest.mark.django_db
def test_api_client_change_user_phone(mock_200_arketa_change_user_phone):
    result = ArketaServiceApiClient().change_user_phone('abc', '+79000000000')
    assert result.get('results')


@pytest.mark.django_db
def test_fail_400_api_client_change_user_phone(mock_400_arketa_change_user_phone):
    result = ArketaServiceApiClient().change_user_phone('abc', '+79000000000')
    assert not result.get('results')


@pytest.mark.django_db
def test_api_client_check_user_exists(mock_200_arketa_check_user_exists):
    result = ArketaServiceApiClient().check_user_exists('+79000000000')
    assert result.get('results')


@pytest.mark.django_db
def test_fail_400_api_client_check_user_exists(mock_400_arketa_check_user_exists):
    result = ArketaServiceApiClient().check_user_exists('+79000000000')
    assert not result.get('results')


@pytest.mark.django_db
def test_api_client_get_documents(mock_200_arketa_get_documents):
    result = ArketaServiceApiClient().get_documents('user_id')
    assert result.get('results')


@pytest.mark.django_db
def test_fail_400_api_client_get_documents(mock_400_arketa_get_documents):
    result = ArketaServiceApiClient().get_documents('user_id')
    assert not result.get('results')


@pytest.mark.django_db
def test_api_client_put_email(mock_200_arketa_put_email):
    result = ArketaServiceApiClient().put_email('user_id', {})
    assert result.get('results')


@pytest.mark.django_db
def test_fail_400_api_client_put_email(mock_400_arketa_put_email):
    result = ArketaServiceApiClient().put_email('user_id', {})
    assert not result.get('results')


@pytest.mark.django_db
def test_api_client_put_inn(mock_200_arketa_put_inn):
    result = ArketaServiceApiClient().put_inn('user_id', {})
    assert result.get('results')


@pytest.mark.django_db
def test_fail_400_api_client_put_inn(mock_400_arketa_put_inn):
    result = ArketaServiceApiClient().put_inn('user_id', {})
    assert not result.get('results')


@pytest.mark.django_db
def test_api_client_put_registration(mock_200_arketa_put_registration):
    result = ArketaServiceApiClient().put_registration('user_id', {})
    assert result.get('results')


@pytest.mark.django_db
def test_fail_400_api_client_put_registration(mock_400_arketa_put_registration):
    result = ArketaServiceApiClient().put_registration('user_id', {})
    assert not result.get('results')


@pytest.mark.django_db
def test_api_client_put_selfie(mock_200_arketa_put_selfie):
    result = ArketaServiceApiClient().put_selfie('user_id', {})
    assert result.get('results')


@pytest.mark.django_db
def test_fail_400_api_client_put_selfie(mock_400_arketa_put_selfie):
    result = ArketaServiceApiClient().put_selfie('user_id', {})
    assert not result.get('results')


@pytest.mark.django_db
def test_api_client_put_snils(mock_200_arketa_put_snils):
    result = ArketaServiceApiClient().put_snils('user_id', {})
    assert result.get('results')


@pytest.mark.django_db
def test_fail_400_api_client_put_snils(mock_400_arketa_put_snils):
    result = ArketaServiceApiClient().put_snils('user_id', {})
    assert not result.get('results')


@pytest.mark.django_db
def test_api_client_put_spread(mock_200_arketa_put_spread):
    result = ArketaServiceApiClient().put_spread('user_id', {})
    assert result.get('results')


@pytest.mark.django_db
def test_fail_400_api_client_put_spread(mock_400_arketa_put_spread):
    result = ArketaServiceApiClient().put_spread('user_id', {})
    assert not result.get('results')
