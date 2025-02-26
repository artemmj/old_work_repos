from typing import List

from api.v1.zone.exceptions import ZonesNotEmptyError
from apps.helpers.services import AbstractService
from apps.zone.models import Zone


class CheckForDocumentsInZonesService(AbstractService):
    """Сервис для проверки наличия документов в зонах."""

    def __init__(self, zones: List[Zone]):
        self.zones = zones

    def process(self, *args, **kwargs):
        zones_with_documents = [
            zone
            for zone in self.zones
            if zone.documents.count() > 0
        ]

        if zones_with_documents:
            raise ZonesNotEmptyError
