import logging

from apps.helpers.services import AbstractService
from apps.zone.models import Zone

logger = logging.getLogger('django')


class GetZonesService(AbstractService):
    """Сервис получения списка зон из БД."""

    def process(self, *args, **kwargs):
        return (
            Zone
            .objects
            .with_usernames_of_counter_scans()
            .with_usernames_of_controllers()
            .calculate_barcode_amount()
            .calculate_tasks_scanned_products_count()
        )
