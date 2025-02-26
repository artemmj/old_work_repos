import pytest
from mixer.backend.django import mixer
from rest_framework.exceptions import ValidationError

from api.v1.terminal.services import ConnTerminalEmployeeService
from apps.terminal.models import Terminal

pytestmark = [pytest.mark.django_db]


def test_conn_terminal_employee(employee):
    terminal = mixer.blend(
        Terminal,
        project=employee.project,
    )
    is_check_terminal = ConnTerminalEmployeeService().process(
        {
            'employee_number': employee.serial_number,
            'terminal': terminal.id,
        },
    )
    assert is_check_terminal


def test_conn_terminal_employee_failed(employee, terminal_zebra):
    with pytest.raises(ValidationError):
        ConnTerminalEmployeeService().process(
            {
                'employee_number': employee.serial_number,
                'terminal': terminal_zebra.id,
            },
        )
