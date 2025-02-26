import pytest

from rest_framework.exceptions import ValidationError

from apps.arketa.clients import ArketaFileApiClient



@pytest.mark.django_db
def test_file_api_client_get(mock_200_arketa_get_file):
    result = ArketaFileApiClient('abc').get_file('file_id')
    assert result.get('results')


@pytest.mark.django_db
def test_fail_400_file_api_client_get(mock_400_arketa_get_file):
    with pytest.raises(ValidationError):
        result = ArketaFileApiClient('abc').get_file('file_id')
        assert not result.get('results')


@pytest.mark.django_db
def test_file_api_client_create(mock_200_arketa_create_file):
    result = ArketaFileApiClient('abc').create_file({'file': 'abc'})
    assert result.get('results')


@pytest.mark.django_db
def test_fail_400_file_api_client_create(mock_400_arketa_create_file):
    with pytest.raises(ValidationError):
        result = ArketaFileApiClient('abc').create_file({'file': 'abc'})
        assert not result.get('results')


@pytest.mark.django_db
def test_file_api_client_put(mock_200_arketa_put_file):
    result = ArketaFileApiClient('abc').put_file('abc', {'file': 'abc'})
    assert result.get('results')


@pytest.mark.django_db
def test_fail_400_file_api_client_put(mock_400_arketa_put_file):
    with pytest.raises(ValidationError):
        result = ArketaFileApiClient('abc').put_file('abc', {'file': 'abc'})
        assert not result.get('results')


@pytest.mark.django_db
def test_file_api_client_patch(mock_200_arketa_patch_file):
    result = ArketaFileApiClient('abc').patch_file('abc', {'file': 'abc'})
    assert result.get('results')


@pytest.mark.django_db
def test_fail_400_file_api_client_patch(mock_400_arketa_patch_file):
    with pytest.raises(ValidationError):
        result = ArketaFileApiClient('abc').patch_file('abc', {'file': 'abc'})
        assert not result.get('results')


@pytest.mark.django_db
def test_file_api_client_delete(mock_200_arketa_delete_file):
    result = ArketaFileApiClient('abc').delete_file('abc')
    assert result.get('results')


@pytest.mark.django_db
def test_fail_400_file_api_client_delete(mock_400_arketa_delete_file):
    with pytest.raises(ValidationError):
        result = ArketaFileApiClient('abc').delete_file('abc')
        assert not result.get('results')
