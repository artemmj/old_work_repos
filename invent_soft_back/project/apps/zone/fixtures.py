from typing import Union, List

import pytest
from mixer.backend.django import mixer

from apps.document.models import DocumentStatusChoices, DocumentColorChoices
from apps.employee.models import EmployeeRoleChoices
from apps.project.models import Project
from apps.task.models import TaskStatusChoices, TaskTypeChoices
from apps.zone.models import Zone, ZoneStatusChoices

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def zone(project: Project):
    """Фикстура для генерации зоны."""
    return mixer.blend(
        Zone,
        project=project,
    )


@pytest.fixture
def zones_factory():
    """Фикстура для генерации зон."""

    def _factory(count: int, **fields) -> Union[Zone, List[Zone]]:
        if count == 1:
            return mixer.blend(
                Zone,
                **fields,
            )
        return mixer.cycle(count).blend(
            Zone,
            **fields,
        )

    return _factory


@pytest.fixture()
def zones_for_inventory_in_zones_report(
    project,
    products_factory,
    scanned_products_factory,
    documents_factory,
    zones_factory,
    tasks_factory,
):
    """Фикстура для генерации зон для отчета "Отчет данных инвентаризации по зонам" на экране Зоны."""
    zones = zones_factory(
        count=3,
        project=project,
        serial_number=(serial_number for serial_number in [1, 2, 3]),
        status=(status for status in [ZoneStatusChoices.READY, ZoneStatusChoices.NOT_READY, ZoneStatusChoices.READY]),
    )
    tasks = tasks_factory(
        count=3,
        zone=(zone for zone in zones),
        type=TaskTypeChoices.COUNTER_SCAN,
        status=TaskStatusChoices.SUCCESS_SCAN,
    )
    documents_factory(
        count=3,
        zone=(zone for zone in zones),
        serial_number=(number for number in [1, 2, 3]),
        counter_scan_task=(task for task in tasks),
        status=DocumentStatusChoices.READY,
        color=DocumentColorChoices.GREEN,
    )
    products = products_factory(count=5, project=project)
    products_with_vendor_code = products_factory(count=5, project=project, vendor_code='46193513')
    scanned_products_factory(
        count=5,
        product=(product for product in products_with_vendor_code),
        amount=(amount for amount in [3, 5, 2, 1, 9]),
        task=tasks[0],
    )
    scanned_products_factory(
        count=5,
        product=(product for product in products),
        amount=(amount for amount in [1, 1, 1, 1, 1]),
        task=tasks[1],
    )
    scanned_products_factory(
        count=5,
        product=(product for product in products),
        amount=(amount for amount in [5, 5, 5, 5, 5]),
        task=tasks[-1],
    )
    return zones


@pytest.fixture()
def zones_for_testing_filters(
    project,
    zones_factory,
    employee_factory,
    tasks_factory,
) -> List[Zone]:
    """Зоны для тестирования работы фильтров этих зон."""
    zones = zones_factory(
        count=3,
        project=project,
        serial_number=(serial_number for serial_number in [1, 2, 3]),
        status=(status for status in [
            ZoneStatusChoices.READY,
            ZoneStatusChoices.NOT_READY,
            ZoneStatusChoices.READY,
        ]),
    )

    counter_scan_employees = employee_factory(
        count=3,
        project=project,
        username=(username for username in ['Сотрудник 1', 'Сотрудник 2', 'Сотрудник 1']),
        roles=[EmployeeRoleChoices.COUNTER],
    )
    controller_employees = employee_factory(
        count=3,
        project=project,
        username=(username for username in ['Сотрудник 1', 'Сотрудник 3', 'Сотрудник 1']),
        roles=[EmployeeRoleChoices.COUNTER],
    )

    tasks_factory(
        count=3,
        zone=(zone for zone in zones),
        employee=(employee for employee in counter_scan_employees),
        type=TaskTypeChoices.COUNTER_SCAN,
        status=(status for status in [
            TaskStatusChoices.SUCCESS_SCAN,
            TaskStatusChoices.SUCCESS_SCAN,
            TaskStatusChoices.FAILED_SCAN,
        ]),
    )
    tasks_factory(
        count=3,
        zone=(zone for zone in zones),
        employee=(employee for employee in controller_employees),
        type=TaskTypeChoices.CONTROLLER,
        status=(status for status in [
            TaskStatusChoices.SUCCESS_SCAN,
            TaskStatusChoices.SUCCESS_SCAN,
            TaskStatusChoices.FAILED_SCAN,
        ]),
    )

    return zones
