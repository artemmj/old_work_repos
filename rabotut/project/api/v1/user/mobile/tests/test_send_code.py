import pytest
from rest_framework import status

from apps.user.models import User


@pytest.mark.django_db
def test_send_code_success(api_v1_send_code, api_client, phone, mock_200_redsms):
    """Тест получения кода по номеру телефона."""
    request_data = {'phone': phone}
    response = api_client.post(api_v1_send_code, request_data)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.override_config(COUNT_SEND_SMS=2, SMS_CODE_IN_RESPONSE=True)
@pytest.mark.django_db
def test_send_code_invalid(api_v1_send_code, api_client, phone):
    """Тест выхода за пределы счетчика."""
    request_data = {'phone': phone}
    for i in range(3):
        response = api_client.post(api_v1_send_code, request_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.override_config(COUNT_SEND_SMS=5, SMS_CODE_IN_RESPONSE=False)
@pytest.mark.django_db
def test_send_code_not_in_response(api_v1_send_code, api_client, phone_2, mock_200_redsms):
    request_data = {'phone': phone_2}
    response = api_client.post(api_v1_send_code, request_data)
    assert not response.data['code']
    assert response.data['is_sent']
    assert response.data['phone'] == phone_2


@pytest.mark.override_config(COUNT_SEND_SMS=5, SMS_CODE_IN_RESPONSE=True)
@pytest.mark.django_db
def test_send_code_in_response(api_v1_send_code, api_client, phone_2):
    request_data = {'phone': phone_2}
    response = api_client.post(api_v1_send_code, request_data)
    assert response.data['code']
    assert not response.data['is_sent']
    assert response.data['phone'] == phone_2

    user_exists = User.objects.filter(phone=phone_2).exists()
    assert user_exists
