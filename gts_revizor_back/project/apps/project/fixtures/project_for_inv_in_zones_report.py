import pytest

from apps.document.models import DocumentStatusChoices
from apps.task.models import TaskTypeChoices, TaskStatusChoices
from apps.zone.models import ZoneStatusChoices

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def project_inv_in_zones_report(
    project,
    zones_factory,
    tasks_factory,
    documents_factory,
):
    """Фикстура создания проекта для отчета Общее кол-во ТМЦ по зонам."""
    zones = zones_factory(
        count=3,
        project=project,
        serial_number=(serial_number for serial_number in [1, 2, 3]),
        status=(status for status in [ZoneStatusChoices.READY, ZoneStatusChoices.NOT_READY, ZoneStatusChoices.READY]),
    )
    counter_scan_tasks = tasks_factory(
        count=3,
        zone=(zone for zone in zones),
        type=TaskTypeChoices.COUNTER_SCAN,
        result=(result for result in [50, 33, 21]),
        status=TaskStatusChoices.SUCCESS_SCAN,
    )
    documents_factory(
        count=3,
        zone=(zone for zone in zones),
        serial_number=(number for number in [1, 2, 3]),
        counter_scan_task=(task for task in counter_scan_tasks),
        status=(
            status
            for status
            in [DocumentStatusChoices.READY, DocumentStatusChoices.NOT_READY, DocumentStatusChoices.READY]
        ),
    )
    return project
