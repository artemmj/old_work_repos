from typing import Dict

from apps.helpers.services import AbstractService
from apps.project.models import User


class GetOrCreateManagerService(AbstractService):
    """Сервис получения или создания менеджера."""

    def __init__(self, manager_content: Dict):
        self.manager_content = manager_content

    def process(self):
        manager, _ = User.objects.get_or_create(
            phone=self.manager_content['phone'],
            defaults={
                'username': self.manager_content['username'],
                'first_name': self.manager_content['first_name'],
                'middle_name': self.manager_content['middle_name'],
                'last_name': self.manager_content['last_name'],
            },
        )
        return manager
