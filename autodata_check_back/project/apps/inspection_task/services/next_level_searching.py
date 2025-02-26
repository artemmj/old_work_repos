from datetime import timedelta

from apps.helpers.services import AbstractService
from apps.inspection_task.models.search import InspectionTaskSearch


class NextLevelSearchingService(AbstractService):
    """Сервис выставления объекту поиска новых уровня и времени."""

    def __init__(self, search_obj: InspectionTaskSearch):  # noqa: D107
        self.search_obj = search_obj

    def process(self, *args, **kwargs):
        self.search_obj.level += 1
        self.search_obj.start_time_iter = self.search_obj.start_time_iter + timedelta(minutes=5)
        self.search_obj.save()
