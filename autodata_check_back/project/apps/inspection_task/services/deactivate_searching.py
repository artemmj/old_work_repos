from apps.helpers.services import AbstractService
from apps.inspection_task.models.search import InspectionTaskSearch


class DeactivateSearchingService(AbstractService):
    """Сервис выключения поиска инспектора."""

    def __init__(self, search_obj: InspectionTaskSearch):   # noqa: D107
        self.search_obj = search_obj

    def process(self, *args, **kwargs):
        self.search_obj.level = 0
        self.search_obj.is_active = False
        self.search_obj.save()
