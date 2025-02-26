import pytest

from apps.terminal.models import Terminal
from apps.terminal.services import BulkCreateTerminalsService

pytestmark = [pytest.mark.django_db]


def test_bulk_create_terminals(project):
    """Тест для проверки массового создания терминалов."""
    terminals_content = [
        {
            'id': '7e21534d-87ef-41e5-9de4-66573c6b608c',
            'number': 99901,
            'ip_address': '192.168.1.141',
            'db_loading': True,
            'last_connect': '2024-05-27T12:26:58.044131+03:00',
        },
        {
            'id': '543957bc-ac51-48b5-a355-234a6cd1300b',
            'number': 99911,
            'ip_address': '192.168.1.62',
            'db_loading': True,
            'last_connect': '2024-05-27T12:26:06.402404+03:00',
        },
    ]

    BulkCreateTerminalsService(project, terminals_content).process()

    assert Terminal.objects.filter(project=project).count() == 2
