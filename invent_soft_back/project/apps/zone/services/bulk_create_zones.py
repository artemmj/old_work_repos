from typing import Dict, List

from apps.helpers.services import AbstractService
from apps.project.models import Project
from apps.zone.models import Zone


class BulkCreateZonesService(AbstractService):
    """Сервис массового создания зон."""

    def __init__(self, new_project: Project, zones_content: List[Dict]):
        self.zones_content = zones_content
        self.new_project = new_project

    def process(self):
        Zone.objects.bulk_create(
            [
                Zone(
                    project=self.new_project,
                    **zone_content,
                )
                for zone_content in self.zones_content
            ],
            ignore_conflicts=True,
        )
