import pytest
import json
from pytest import fixture
from rest_framework import status
from rest_framework.test import APIClient
from mixer.backend.django import mixer

from apps.employee.models import Employee
from apps.project.models import Project
from apps.zone.models import Zone
from api.v1.product.serializers import ProductReadSerializer
from api.v1.zone.serializers import ZoneReadSerializer
from api.v1.document.serializers import DocumentReadSerializer
from api.v1.task.serializers import TaskReadSerializer
from api.v1.product.serializers import ScannedProductReadSerializer

pytestmark = [pytest.mark.django_db]


def test_search_by_fields(
    client: APIClient,
    products_factory: fixture,
    documents_factory: fixture,
    tasks_factory: fixture,
    scanned_products_factory: fixture,
    zones_factory: fixture,
    project: Project,
    employee: Employee,
):
    zones = zones_factory(
        count=6,
        project=project,
        serial_number=(v for v in [1, 2, 3, 4, 5, 6])
    )
    products = products_factory(
        count=6,
        project=project,
        title=(v for v in ['qwe', 'asd', 'zxc', 'rty', 'fgh', 'vbn']),
        barcode=(v for v in ['1111', '2222', '3333', '4444', '5555', '6666']),
        vendor_code=(v for v in ['0001', '0002', '0003', '0004', '0005', '0007']),
    )
    counter_tasks = tasks_factory(
        count=6,
        zone=(v for v in zones),
        employee=employee,
        result=(v for v in [1, 2, 3, 4, 5, 6])
    )
    scanned_products_factory(
        count=6,
        product=(v for v in products),
        task=(v for v in counter_tasks),
        amount=(v for v in [1, 2, 3, 4, 5, 6])
    )
    documents_factory(
        count=6,
        zone=(v for v in zones),
        counter_scan_task=(v for v in counter_tasks)
    )
    search_fields_map = {
        'product_title': ['qwe', 'asd'],
        'barcode': ['1111', '2222'],
        'vendor_code': ['0001', '0002'],
    }
    for search_field, values in search_fields_map.items():
        for value in values:
            url = f'/api/v1/document/?project={project.pk}&{search_field}={value}'
            response = client.get(url)
            assert response.data['count'] == 1
