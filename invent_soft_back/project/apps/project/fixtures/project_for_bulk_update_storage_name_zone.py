import pytest

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def project_for_bulk_update_storage_name_zone(
    project,
    zones_factory,
):
    """Фикстура создания проекта для сервиса изменения названий складов зон.."""
    zones_factory(
        count=5,
        project=project,
        serial_number=(serial_number for serial_number in [1, 2, 3, 4, 5]),
    )

    return project
