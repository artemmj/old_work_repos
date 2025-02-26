from typing import Dict

from django.db import transaction

from apps.helpers.services import AbstractService
from apps.zone.models import Zone


class BulkUpdateStorageNameZoneService(AbstractService):
    """Сервис изменения названий складов зон."""

    @transaction.atomic
    def process(self, filter_options: Dict, storage_name: str):
        Zone.objects.filter(**filter_options).update(storage_name=storage_name)
