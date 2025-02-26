from enum import Enum
from typing import Iterable, List

import pytest
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory

from api.v1.document.ordering import DocumentOrderingService
from apps.document.models import Document, DocumentColorChoices
from apps.employee.models import EmployeeRoleChoices, Employee
from apps.project.models import Project
from apps.user.models import User
from apps.zone.models import Zone

pytestmark = [pytest.mark.django_db]

ENTITY_COUNT = 5

class ScannedProductsIds(Enum):
    one = 'fcacbde4-1df5-4433-a924-d4a5815535f9'
    two = '92067cd9-9624-4d12-8caa-343c257896a9'
    three = '0c287d20-16e0-4fe2-8993-5724cba8a080'
    four = '0e15033d-842f-47f6-8955-8da008b0377e'
    five = 'f94717f4-c856-4d3e-bec8-d291bbe693d9'


@pytest.mark.parametrize(
    'ordering_param, documents_ids_after_ordering',
    [
        ('colors', [1, 4, 2, 3, 5]),
        ('-colors', [5, 2, 3, 1, 4]),
    ]
)
def test_documents_filtering_by_query_params_successful(
    project: Project,
    ordering_param: str,
    documents_ids_after_ordering: Iterable[int],
    zones_factory,
    documents_factory,
    employee_factory,
):
    factory = APIRequestFactory()

    zones = zones_factory(
        count=5,
        project=project,
        title=(title for title in ('Зона 3', 'Зона 1', 'Зона 5', 'Зона 2', 'Зона 4'))
    )
    employees = employee_factory(
        count=5,
        project=project,
        roles=[EmployeeRoleChoices.COUNTER],
        username=(username for username in (
            'Сотрудник 5',
            'Сотрудник 2',
            'Сотрудник 4',
            'Сотрудник 1',
            'Сотрудник 3',
        ))
    )
    documents_factory(
        id=(document_id for document_id in range(1, 6)),
        count=5,
        zone=(zone for zone in zones),
        employee=(employee for employee in employees),
        color=(color for color in [
            DocumentColorChoices.RED,
            DocumentColorChoices.ORANGE,
            DocumentColorChoices.ORANGE,
            DocumentColorChoices.RED,
            DocumentColorChoices.WHITE,
        ])
    )

    url = f'/api/v1/document/?project={zones[0].project}&ordering={ordering_param}'
    request = Request(factory.get(url))
    ordering_param = request.query_params.get('ordering')

    ordered_documents = DocumentOrderingService(
        ordering_param=ordering_param,
        queryset=Document.objects.all(),
    ).process()

    assert list(ordered_documents.values_list('id', flat=True)) == documents_ids_after_ordering


@pytest.mark.parametrize(
    'ordering_param, documents_scanned_products_ids_after_ordering',
    [
        ('-number', [
            ScannedProductsIds.three.value,
            ScannedProductsIds.four.value,
            ScannedProductsIds.two.value,
            ScannedProductsIds.five.value,
            ScannedProductsIds.one.value,
        ]),
        ('number', [
            ScannedProductsIds.one.value,
            ScannedProductsIds.five.value,
            ScannedProductsIds.two.value,
            ScannedProductsIds.four.value,
            ScannedProductsIds.three.value,
        ]),
        ('product__title', [
            ScannedProductsIds.five.value,
            ScannedProductsIds.four.value,
            ScannedProductsIds.two.value,
            ScannedProductsIds.one.value,
            ScannedProductsIds.three.value,
        ]),
        ('-product__title', [
            ScannedProductsIds.three.value,
            ScannedProductsIds.one.value,
            ScannedProductsIds.two.value,
            ScannedProductsIds.four.value,
            ScannedProductsIds.five.value,
        ]),
        ('product__vendor_code', [
            ScannedProductsIds.three.value,
            ScannedProductsIds.one.value,
            ScannedProductsIds.two.value,
            ScannedProductsIds.five.value,
            ScannedProductsIds.four.value,
        ]),
        ('-product__vendor_code', [
            ScannedProductsIds.four.value,
            ScannedProductsIds.five.value,
            ScannedProductsIds.two.value,
            ScannedProductsIds.one.value,
            ScannedProductsIds.three.value,
        ]),
        ('product__barcode', [
            ScannedProductsIds.four.value,
            ScannedProductsIds.one.value,
            ScannedProductsIds.two.value,
            ScannedProductsIds.five.value,
            ScannedProductsIds.three.value,
        ]),
        ('-product__barcode', [
            ScannedProductsIds.three.value,
            ScannedProductsIds.five.value,
            ScannedProductsIds.two.value,
            ScannedProductsIds.one.value,
            ScannedProductsIds.four.value,
        ]),
        ('amount', [
            ScannedProductsIds.five.value,
            ScannedProductsIds.one.value,
            ScannedProductsIds.three.value,
            ScannedProductsIds.four.value,
            ScannedProductsIds.two.value,
        ]),
        ('-amount', [
            ScannedProductsIds.two.value,
            ScannedProductsIds.four.value,
            ScannedProductsIds.three.value,
            ScannedProductsIds.one.value,
            ScannedProductsIds.five.value,
        ]),
        ('displayed_dm', [
            ScannedProductsIds.four.value,
            ScannedProductsIds.one.value,
            ScannedProductsIds.two.value,
            ScannedProductsIds.five.value,
            ScannedProductsIds.three.value,
        ]),
        ('-displayed_dm', [
            ScannedProductsIds.three.value,
            ScannedProductsIds.five.value,
            ScannedProductsIds.two.value,
            ScannedProductsIds.one.value,
            ScannedProductsIds.four.value,
        ]),

    ]
)
def test_documents_scanned_products_filtering_by_query_params_successful(
    ordering_param: str,
    documents_scanned_products_ids_after_ordering: List[str],
    client: APIClient,
    project: Project,
    zone: Zone,
    employee: Employee,
    user: User,
    products_factory,
    tasks_factory,
    scanned_products_factory,
    documents_factory,
):
    products_titles = [
        'Игрушка Карточка 89 ШК4',
        'Другой кругляк Карточка 89 ШК5',
        'Игрушка Карточка ШК4',
        'Боди черный XL',
        'Боди черный S',
    ]
    products_vendor_codes = [
        '100013',
        '100017',
        '100012',
        '100030',
        '100029',
    ]
    products_barcodes = [
        '2000002050087',
        '2000002050124',
        '4660053615352',
        '2000002050070',
        '4620123389590',
    ]
    scanned_products_amount = [
        '4.00',
        '24.00',
        '9.00',
        '15.00',
        '2.00',
    ]
    scanned_products_dms = [
        '2000002050087',
        '2000002050124',
        '4660053615352',
        '2000002050070',
        '4620123389590',
    ]

    products = products_factory(
        count=ENTITY_COUNT,
        project=project,
        title=(title for title in products_titles),
        vendor_code=(vendor_code for vendor_code in products_vendor_codes),
        barcode=(barcode for barcode in products_barcodes),
    )
    counter_task = tasks_factory(count=1, zone=zone, employee=employee)
    scanned_products_factory(
        id=(scanned_product_id.value for scanned_product_id in ScannedProductsIds),
        count=ENTITY_COUNT,
        product=(v for v in products),
        task=counter_task,
        amount=(amount for amount in scanned_products_amount),
        dm=(dm for dm in scanned_products_dms)
    )
    document = documents_factory(
        count=1,
        project=project,
        counter_scan_task=counter_task,
    )

    url = f'/api/v1/document_scanned_products/?document={document.id}&ordering={ordering_param}'
    client.force_login(user=user)
    response = client.get(url)
    documents_scanned_products_ids = [scanned_product['id'] for scanned_product in response.data['results']]

    assert response.status_code == status.HTTP_200_OK
    assert documents_scanned_products_ids == documents_scanned_products_ids_after_ordering
