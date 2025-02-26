import pytest

from apps.event.models import Event
from apps.event.services import BulkCreateEventsService

pytestmark = [pytest.mark.django_db]


def test_bulk_create_events(project):
    """Тест для проверки массового создания событий."""
    events_content = [
        {
            'fake_id': 1,
            'created_at': '2024-05-27T10:50:06.672987+03:00',
            'title': 'create_new_project',
            'comment': 'Создан новый проект.'
        },
        {
            'fake_id': 2,
            'created_at': '2024-05-27T10:55:52.961219+03:00',
            'title': 'project_settings_update',
            'comment': 'Изменены настройки проекта.'
        },
    ]

    BulkCreateEventsService(project, events_content).process()

    assert Event.objects.filter(project=project).count() == 2
