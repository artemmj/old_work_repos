import pytest

from apps.event.models import Event, TitleChoices
from apps.event.services import CreateEventService

pytestmark = [pytest.mark.django_db]


def test_create_event(project):
    """Тест для проверки создания события."""
    title = TitleChoices.CREATE_NEW_PROJECT
    comment = 'Создан новый проект'

    CreateEventService(project, title, comment).process()

    assert Event.objects.filter(project=project).count() == 1
    assert Event.objects.filter(project=project).first().title == 'create_new_project'
