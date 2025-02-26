import pytest

from apps.project.models import Project
from apps.task.models import TaskTypeChoices, TaskStatusChoices
from apps.zone.models import Zone

pytestmark = [pytest.mark.django_db]


def test_1_calculate_barcode_amount_in_zone_successful(
    project: Project,
    tasks_factory,
    zones_factory,
):
    """Тест для проверки расчёта количества шк в зоне с одной таской со статусом 'Удачный скан, сошлось'."""
    zone = zones_factory(count=1, project=project)

    tasks_factory(
        count=1,
        zone=zone,
        type=TaskTypeChoices.COUNTER_SCAN,
        status=TaskStatusChoices.SUCCESS_SCAN,
        result=45,
    )

    created_zone = Zone.objects.calculate_barcode_amount().first()

    assert created_zone.barcode_amount == 45


def test_2_calculate_barcode_amount_in_zone_successful(
    project: Project,
    tasks_factory,
    zones_factory,
):
    """Тест для проверки расчёта количества шк в зоне с тасками типа 'Сошлось' и 'Не сошлось'."""
    zone = zones_factory(count=1, project=project)

    tasks_factory(
        count=1,
        zone=zone,
        type=TaskTypeChoices.COUNTER_SCAN,
        status=TaskStatusChoices.SUCCESS_SCAN,
        result=45,
    )

    tasks_factory(
        count=4,
        zone=zone,
        type=TaskTypeChoices.COUNTER_SCAN,
        status=TaskStatusChoices.FAILED_SCAN,
        result=54,
    )

    created_zone = Zone.objects.calculate_barcode_amount().first()

    assert created_zone.barcode_amount == 45


def test_3_calculate_barcode_amount_in_zone_successful(
    project: Project,
    tasks_factory,
    zones_factory,
):
    """Тест для проверки расчёта количества шк в зоне с тасками типа 'Не сошлось'."""
    zone = zones_factory(count=1, project=project)

    tasks_factory(
        count=5,
        zone=zone,
        type=TaskTypeChoices.COUNTER_SCAN,
        status=TaskStatusChoices.FAILED_SCAN,
        result=(barcode_amount for barcode_amount in (5, 50, 23, 54, 11)),
    )

    created_zone = Zone.objects.calculate_barcode_amount().first()

    assert created_zone.barcode_amount == 11
