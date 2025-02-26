from typing import Iterable

import pytest

from api.v1.document.ordering import DocumentOrderingService
from apps.document.models import Document
from apps.employee.models import EmployeeRoleChoices
from apps.project.models import Project

pytestmark = [pytest.mark.django_db]


@pytest.mark.parametrize(
    'ordering_param, documents_ids_after_ordering',
    [
        ('zone_title', [2, 4, 1, 5, 3]),
        ('-zone_title', [3, 5, 1, 4, 2]),
        ('employee_name', [4, 2, 5, 3, 1]),
        ('-employee_name', [1, 3, 5, 2, 4]),
    ]
)
def test_documents_filtering_by_zone_title_params_successful(
    project: Project,
    ordering_param: str,
    documents_ids_after_ordering: Iterable[int],
    zones_factory,
    documents_factory,
    employee_factory,
):
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
    )

    ordered_documents = DocumentOrderingService(
        ordering_param=ordering_param,
        queryset=Document.objects.all(),
    ).process()

    assert list(ordered_documents.values_list('id', flat=True)) == documents_ids_after_ordering
