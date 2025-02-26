from typing import Union, List

import pytest
from mixer.backend.django import mixer

from apps.task.models import Task

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def tasks_factory():
    """Фикстура для генерации заданий."""

    def _factory(count: int, **fields) -> Union[Task, List[Task]]:
        if count == 1:
            return mixer.blend(
                Task,
                **fields,
            )
        return mixer.cycle(count).blend(
            Task,
            **fields,
        )

    return _factory
