import random

import pytest
from rest_framework.exceptions import ValidationError

from api.v1.terminal.services import CheckTerminalNumberService

pytestmark = [pytest.mark.django_db]


def test_check_terminal_number_service_created():
    is_checking_terminal = CheckTerminalNumberService(
        number=random.randrange(99900, 100000),
        device_model='MC2200',
        created=True,
    ).process()

    assert is_checking_terminal


def test_check_terminal_number_service_created_busy_number(terminal):
    with pytest.raises(ValidationError):
        CheckTerminalNumberService(
            number=terminal.number,
            device_model=terminal.device_model,
            created=True,
        ).process()


def test_check_terminal_number_service_zebra():
    is_checking_terminal = CheckTerminalNumberService(
        number=random.randrange(3000, 4000),
        device_model='MC2200',
        created=False,
    ).process()

    assert is_checking_terminal


def test_check_terminal_number_service_zebra_busy_number(terminal_zebra):
    with pytest.raises(ValidationError):
        CheckTerminalNumberService(
            number=terminal_zebra.number,
            device_model=terminal_zebra.device_model,
            created=False,
        ).process()


def test_check_terminal_number_service_zebra_invalid_range():
    with pytest.raises(ValidationError):
        CheckTerminalNumberService(
            number=random.randrange(4000, 5000),
            device_model='MC2200',
            created=False,
        ).process()


def test_check_terminal_number_service_cachalot():
    is_checking_terminal = CheckTerminalNumberService(
        number=random.randrange(4000, 5000),
        device_model='NLS-N7',
        created=False,
    ).process()

    assert is_checking_terminal


def test_check_terminal_number_service_cachalot_busy_number(terminal_cachalot):
    with pytest.raises(ValidationError):
        CheckTerminalNumberService(
            number=terminal_cachalot.number,
            device_model=terminal_cachalot.device_model,
            created=False,
        ).process()


def test_check_terminal_number_service_cachalot_invalid_range():
    with pytest.raises(ValidationError):
        CheckTerminalNumberService(
            number=random.randrange(3000, 4000),
            device_model='NLS-N7',
            created=False,
        ).process()


def test_check_terminal_number_service_invalid_model():
    with pytest.raises(ValidationError):
        CheckTerminalNumberService(
            number=random.randrange(3000, 5000),
            device_model='MD-3444',
            created=False,
        ).process()
