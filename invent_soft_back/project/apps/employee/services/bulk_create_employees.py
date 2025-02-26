from typing import Dict, List

from apps.employee.models import Employee
from apps.helpers.services import AbstractService
from apps.project.models import Project


class BulkCreateEmployeesService(AbstractService):
    """Сервис массового создания сотрудников."""

    def __init__(self, new_project: Project, employees_content: List[Dict]):
        self.employees_content = employees_content
        self.new_project = new_project

    def process(self):
        Employee.objects.bulk_create(
            [
                Employee(
                    project=self.new_project,
                    **employee_content,
                )
                for employee_content in self.employees_content
            ],
            ignore_conflicts=True,
        )
