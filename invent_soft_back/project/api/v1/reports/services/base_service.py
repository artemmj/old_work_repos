from apps.helpers.services import AbstractService
from apps.project.models import Project


class BaseReportService(AbstractService):
    """Базовый класс для сервисов генерации отчетов."""

    def __init__(self, serializer_data: dict, endpoint_pref: str):
        self.project = Project.objects.get(pk=serializer_data['project'])
        self.endpoint_pref = endpoint_pref
