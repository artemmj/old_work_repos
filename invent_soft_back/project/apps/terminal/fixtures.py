import random
from typing import Union, List

import pytest
from mixer.backend.django import mixer

from apps.terminal.models import Terminal

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def terminal():
    """Фикстура создания терминала при первом подключении к бэку"""
    return mixer.blend(
        Terminal,
        number=99900,
        device_model='MC2200',
    )


@pytest.fixture
def terminals_factory():
    """Фикстура для генерации терминалов."""

    def _factory(count: int, **fields) -> Union[Terminal, List[Terminal]]:
        if count == 1:
            return mixer.blend(
                Terminal,
                **fields,
            )
        return mixer.cycle(count).blend(
            Terminal,
            **fields,
        )

    return _factory


@pytest.fixture()
def terminal_zebra():
    """Фикстура создания терминала Зебра"""
    return mixer.blend(
        Terminal,
        number=random.randrange(3000, 4000),
        device_model='MC2200',
    )


@pytest.fixture()
def terminal_cachalot():
    """Фикстура создания терминала Кашалот"""
    return mixer.blend(
        Terminal,
        number=random.randrange(4000, 5000),
        device_model='NLS-N7',
    )
