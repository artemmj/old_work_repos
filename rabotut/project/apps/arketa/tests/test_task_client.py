import pytest

from rest_framework .exceptions import ValidationError

from apps.arketa.clients import ArketaTaskApiClient



@pytest.mark.django_db
def test_api_client_task_vacant(mock_200_arketa_task_vacant):
    input_data = {
        'latitude': 55.755819,
        'longitude': 37.617644,
        'trade_point': ['tp'],
    }
    result = ArketaTaskApiClient('abc').task_vacant(input_data)
    assert result.get('results')


@pytest.mark.django_db
def test_fail_400_api_client_task_vacant(mock_400_arketa_task_vacant):
    with pytest.raises(ValidationError):
        input_data = {
            'latitude': 55.755819,
            'longitude': 37.617644,
            'trade_point': ['tp'],
        }
        result = ArketaTaskApiClient('abc').task_vacant(input_data)
        assert not result.get('results')


@pytest.mark.django_db
def test_api_client_task_available_for_reserve(mock_200_arketa_task_available_for_reserve):
    result = ArketaTaskApiClient('jwt_token').task_available_for_reserve()
    assert result.get('results')


@pytest.mark.django_db
def test_fail_400_api_client_task_available_for_reserve(mock_400_arketa_task_available_for_reserve):
    with pytest.raises(ValidationError):
        result = ArketaTaskApiClient('jwt_token').task_available_for_reserve()
        assert not result.get('results')


@pytest.mark.django_db
def test_api_client_task_preview(mock_200_arketa_task_preview):
    result = ArketaTaskApiClient('jwt_token').task_preview('abc')
    assert result.get('results')


@pytest.mark.django_db
def test_fail_400_api_client_task_preview(mock_400_arketa_task_preview):
    with pytest.raises(ValidationError):
        result = ArketaTaskApiClient('jwt_token').task_preview('abc')
        assert not result.get('results')


@pytest.mark.django_db
def test_api_client_vacant_take(mock_200_arketa_vacant_take):
    result = ArketaTaskApiClient('jwt_token').vacant_take(['abc'])
    assert result.get('results')


@pytest.mark.django_db
def test_fail_400_api_client_vacant_take(mock_400_arketa_vacant_take):
    with pytest.raises(ValidationError):
        result = ArketaTaskApiClient('jwt_token').vacant_take(['abc'])
        assert not result.get('results')


@pytest.mark.django_db
def test_api_client_check_docs(mock_200_arketa_check_docs):
    result = ArketaTaskApiClient('jwt_token').check_arketa_documents()
    assert result.get('results')


@pytest.mark.django_db
def test_fail_400_api_client_check_docs(mock_400_arketa_check_docs):
    with pytest.raises(ValidationError):
        result = ArketaTaskApiClient('jwt_token').check_arketa_documents()
        assert not result.get('results')


@pytest.mark.django_db
def test_api_client_statuses(mock_200_arketa_statuses):
    result = ArketaTaskApiClient('abc').statuses()
    assert result.get('results')


@pytest.mark.django_db
def test_fail_400_api_client_statuses(mock_400_arketa_statuses):
    with pytest.raises(ValidationError):
        result = ArketaTaskApiClient('abc').statuses()
        assert not result.get('results')


@pytest.mark.django_db
def test_api_client_current(mock_200_arketa_current):
    result = ArketaTaskApiClient('abc').current({})
    assert result.get('results')


@pytest.mark.django_db
def test_fail_400_api_client_current(mock_400_arketa_current):
    with pytest.raises(ValidationError):
        result = ArketaTaskApiClient('abc').current({})
        assert not result.get('results')


@pytest.mark.django_db
def test_api_client_cancel_reservation(mock_200_arketa_cancel_reservation):
    result = ArketaTaskApiClient('abc').cancel_reservation('task_id', {})
    assert result.get('results')


@pytest.mark.django_db
def test_fail_400_api_client_cancel_reservation(mock_400_arketa_cancel_reservation):
    with pytest.raises(ValidationError):
        result = ArketaTaskApiClient('abc').cancel_reservation('task_id', {})
        assert not result.get('results')


@pytest.mark.django_db
def test_api_client_answer(mock_200_arketa_answer):
    result = ArketaTaskApiClient('abc').answer({})
    assert result.get('results')


@pytest.mark.django_db
def test_fail_400_api_client_answer(mock_400_arketa_answer):
    with pytest.raises(ValidationError):
        result = ArketaTaskApiClient('abc').answer({})
        assert not result.get('results')


@pytest.mark.django_db
def test_api_client_visit(mock_200_arketa_visit):
    result = ArketaTaskApiClient('abc').visit({})
    assert result.get('results')


@pytest.mark.django_db
def test_fail_400_api_client_visit(mock_400_arketa_visit):
    with pytest.raises(ValidationError):
        result = ArketaTaskApiClient('abc').visit({})
        assert not result.get('results')


@pytest.mark.django_db
def test_api_client_like(mock_200_arketa_like):
    result = ArketaTaskApiClient('abc').like('task_id')
    assert result.get('results')


@pytest.mark.django_db
def test_fail_400_api_client_like(mock_400_arketa_like):
    with pytest.raises(ValidationError):
        result = ArketaTaskApiClient('abc').like('task_id')
        assert not result.get('results')


@pytest.mark.django_db
def test_api_client_dislike(mock_200_arketa_dislike):
    result = ArketaTaskApiClient('abc').dislike('task_id')
    assert result.get('results')


@pytest.mark.django_db
def test_fail_400_api_client_dislike(mock_400_arketa_dislike):
    with pytest.raises(ValidationError):
        result = ArketaTaskApiClient('abc').dislike('task_id')
        assert not result.get('results')
