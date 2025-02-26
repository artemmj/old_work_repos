from typing import Union, List

import pytest
from mixer.backend.django import mixer

from apps.employee.models import Employee, EmployeeRoleChoices
from apps.project.models import Project

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def employee(project: Project):
    """Фикстура для генерации сотрудника с ролью аудитор."""
    return mixer.blend(
        Employee,
        project=project,
        roles=[EmployeeRoleChoices.AUDITOR],
    )


@pytest.fixture
def employee_factory():
    """Фикстура для генерации сотрудников"""
    def _factory(count: int, **fields) -> Union[Employee, List[Employee]]:
        if count == 1:
            return mixer.blend(
                Employee,
                **fields,
            )
        return mixer.cycle(count).blend(
            Employee,
            **fields,
        )

    return _factory
