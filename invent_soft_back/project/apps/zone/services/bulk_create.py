import logging

from apps.helpers.services import AbstractService
from apps.project.models import Project
from apps.zone.models import Zone

logger = logging.getLogger('django')


class BulkCreateZoneService(AbstractService):
    """Сервис пакетного создания зон."""

    def __init__(  # noqa: WPS211
        self,
        project: Project,
        storage_name: str,
        start_serial_number: int,
        end_serial_number: int,
        batch_size: int,
    ):
        self.project = project
        self.storage_name = storage_name
        self.start_serial_number = start_serial_number
        self.end_serial_number = end_serial_number
        self.batch_size = batch_size

    def process(self, *args, **kwargs):  # noqa: WPS231
        return Zone.objects.bulk_create(
            [
                Zone(
                    project=self.project,
                    serial_number=number,
                    code=number,
                    storage_name=self.storage_name,
                    title=f'Зона {number}',
                )
                for number in range(self.start_serial_number, self.end_serial_number)
            ],
            ignore_conflicts=True,
            batch_size=self.batch_size,
        )
