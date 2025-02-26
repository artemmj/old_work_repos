import pytest

from rest_framework .exceptions import ValidationError

from apps.arketa.clients import ArketaTradepointApiClient


@pytest.mark.django_db
def test_api_client_trade_point_vacant(mock_200_arketa_trade_point_vacant):
    input_data = {
        'latitude': 55.755819,
        'longitude': 37.617644,
    }
    result = ArketaTradepointApiClient('abc').trade_point_vacant(input_data)
    assert result.get('results')


@pytest.mark.django_db
def test_fail_400_api_client_trade_point_vacant(mock_400_arketa_trade_point_vacant):
    with pytest.raises(ValidationError):
        input_data = {
            'latitude': 55.755819,
            'longitude': 37.617644,
        }
        result = ArketaTradepointApiClient('abc').trade_point_vacant(input_data)
        assert not result.get('results')


@pytest.mark.django_db
def test_fail_500_api_client_trade_point_vacant(mock_500_arketa_api_client_trade_point_vacant):
    with pytest.raises(ValidationError):
        input_data = {
            'latitude': 55.755819,
            'longitude': 37.617644,
        }
        result = ArketaTradepointApiClient('abc').trade_point_vacant(input_data)
        assert not result.get('results')
