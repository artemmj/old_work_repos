import pytest
import json

from django.contrib.gis.geos import Point


@pytest.mark.django_db
def test_write_city_to_user(applicant_user, applicant_client, regions_factory, cities_factory):
    region = regions_factory(count=1, name=(_ for _ in ['Регион1']))
    city = cities_factory(
        count=1,
        name=(_ for _ in ['Город1']),
        location=Point((57.17169, 37.930262)),
        region=region,
    )
    response = applicant_client.patch(f'/api/v1/user/{applicant_user.pk}/', data={'city': city.pk})
    json_response = json.loads(response.content.decode('utf-8'))
    assert json_response['city'] == str(city.pk)
    assert json_response['regions'][0] == str(region.pk)
    assert json_response['location']['longitude'] == 57.17169
    assert json_response['location']['latitude'] == 37.930262
