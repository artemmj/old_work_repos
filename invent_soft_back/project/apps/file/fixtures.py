from typing import Union, List

import pytest
from mixer.backend.django import mixer

from apps.file.models import File

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def files_factory():
    """Фикстура для генерации файлов."""

    def _factory(count: int, **fields) -> Union[File, List[File]]:
        if count == 1:
            return mixer.blend(
                File,
                **fields,
            )
        return mixer.cycle(count).blend(
            File,
            **fields,
        )

    return _factory
