import json

import pytest
from django.contrib.gis.geos import Point


@pytest.mark.django_db
def test_write_location_to_user(applicant_user, applicant_client, regions_factory, cities_factory):
    regions = regions_factory(
        count=3,
        name=(_ for _ in ['Регион1', 'Регион2', 'Регион3']),
    )
    points = (Point((50.000000, 30.000000)), Point((55.000000, 35.000000)), Point((56.000000, 36.000000)))
    cities = cities_factory(
        count=3,
        name=(_ for _ in ['Город1', 'Город2', 'Город3']),
        region=(_ for _ in regions),
        location=(_ for _ in points),
    )
    response = applicant_client.patch(
        f'/api/v1/user/{applicant_user.pk}/',
        data={
            'location': {
                'longitude': 52.000000,
                'latitude': 32.000000,
            }
        },
        format='json',
    )
    json_response = json.loads(response.content.decode('utf-8'))
    assert json_response['city'] == str(cities[0].id)
    assert json_response['regions'][0] == str(cities[0].region.pk)
    assert json_response['location']['longitude'] == 52.000000
    assert json_response['location']['latitude'] == 32.000000
