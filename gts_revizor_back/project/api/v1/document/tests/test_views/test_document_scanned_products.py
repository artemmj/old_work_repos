import pytest
from rest_framework import status
from rest_framework.test import APIClient

from apps.employee.models import Employee
from apps.project.models import Project, User
from apps.zone.models import Zone

pytestmark = [pytest.mark.django_db]

ENTITY_COUNT = 10


@pytest.mark.parametrize(
    'filter_argument, filter_value, scanned_products_count_after_filtering',
    [
        ('title', 'игрушка', 4),
        ('title', 'Игрушка', 4),
        ('title', 'игруш', 4),
        ('title', 'Игруш', 4),
        ('title', 'Боди черный', 3),
        ('title', 'Боди Черный', 3),
        ('title', 'Джинсы бел', 2),
        ('title', 'Джинсы Бел', 2),
        ('vendor_code', '1', 10),
        ('vendor_code', '111', 3),
        ('vendor_code', '122', 3),
        ('vendor_code', '144', 1),
        ('barcode', '200', 1),
        ('barcode', '003505158', 3),
    ]
)
def test_scanned_products_filtering_by_title_successful(
    client: APIClient,
    filter_argument: str,
    filter_value: str,
    scanned_products_count_after_filtering: int,
    user: User,
    project: Project,
    zone: Zone,
    employee: Employee,
    scanned_products_factory,
    products_factory,
    tasks_factory,
    documents_factory,
):
    products_titles = [
        'Игрушка Карточка 89 ШК4',
        'Другой кругляк Карточка 89 ШК5',
        'Игрушка Карточка 89 ШК4',
        'Игрушка Карточка 92 ШК4',
        'Игрушка Карточка 89 ШК6',
        'Боди черный XL',
        'Боди черный XL',
        'Боди черный S',
        'Джинсы белый L',
        'Джинсы белый L',
    ]

    products_vendor_codes = [
        '111001',
        '111002',
        '111003',
        '122004',
        '122005',
        '122006',
        '133007',
        '133008',
        '133009',
        '1440010',
    ]

    products_barcodes = [
        '2000002050018',
        '4620123389658',
        '4620123389789',
        '4620123389412',
        '0035051584521',
        '0035051589452',
        '0035051581123',
        '194735121232',
        '194735148545',
        '194735854568',
    ]

    products = products_factory(
        count=ENTITY_COUNT,
        project=project,
        title=(title for title in products_titles),
        vendor_code=(code for code in products_vendor_codes),
        barcode=(barcode for barcode in products_barcodes)
    )
    counter_task = tasks_factory(count=1, zone=zone, employee=employee)
    scanned_products_factory(
        count=ENTITY_COUNT,
        product=(v for v in products),
        task=counter_task,
    )
    document = documents_factory(
        count=1,
        project=project,
        counter_scan_task=counter_task,
    )

    url = f'/api/v1/document_scanned_products/?document={document.id}&{filter_argument}={filter_value}'
    client.force_login(user=user)
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == scanned_products_count_after_filtering
