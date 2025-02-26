from typing import Union, List

import pytest
from mixer.backend.django import mixer

from apps.template.models import Template, TemplateExport

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def templates_factory():
    """Фикстура для генерации шаблонов."""

    def _factory(count: int, **fields) -> Union[Template, List[Template]]:
        if count == 1:
            return mixer.blend(
                Template,
                **fields,
            )
        return mixer.cycle(count).blend(
            Template,
            **fields,
        )

    return _factory


@pytest.fixture
def templates_export_factory():
    """Фикстура для генерации шаблонов."""

    def _factory(count: int, **fields) -> Union[TemplateExport, List[TemplateExport]]:
        if count == 1:
            return mixer.blend(
                TemplateExport,
                **fields,
            )
        return mixer.cycle(count).blend(
            TemplateExport,
            **fields,
        )

    return _factory
