import json

import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_create_list_faq(client: APIClient, cities_factory):
    """Тест создания и получения городов, фильтрации по query_params."""
    cities_factory(
        count=3,
        name=(name for name in ['Москва', 'Питер',  'Пинск'])
    )

    response = client.get('/api/v1/address/city/')
    response_data = json.loads(response.content)
    assert response_data['count'] == 3

    response = client.get('/api/v1/address/city/?search_name=Пи')
    response_data = json.loads(response.content)
    assert response_data['count'] == 2

    response = client.get('/api/v1/address/city/?search_name=Пит')
    response_data = json.loads(response.content)
    assert response_data['count'] == 1
