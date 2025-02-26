import pytest
from rest_framework import status

from apps.user.models import User


@pytest.mark.django_db
def test_login(api_v1_login, api_client, code, phone, user):
    """Тест логина."""
    code = code["code"]
    response = api_client.post(api_v1_login, {'phone': phone, 'code': code})
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_first_time_login(api_v1_send_code, api_client, phone_2):
    """Тест на создание пользователя при первом входе"""
    request_data = {'phone': phone_2}
    assert not User.objects.filter(phone=phone_2).exists()
    response = api_client.post(api_v1_send_code, request_data)
    assert User.objects.filter(phone=phone_2).exists()


@pytest.mark.django_db
def test_login_with_invalid_phone(api_v1_login, api_client, code, phone_2, user):
    """Тест связку неправльного телефона и кода."""
    code = code["code"]
    response = api_client.post(api_v1_login, {'phone': phone_2, 'code': code})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_login_with_invalid_code(api_v1_login, api_client, code_2, phone, user):
    """Тест на связку неправильного кода и телефона."""
    code = code_2["code"]
    response = api_client.post(api_v1_login, {'phone': phone, 'code': code})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
