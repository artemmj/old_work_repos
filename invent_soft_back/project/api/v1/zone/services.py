from apps.helpers.services import AbstractService


class ZoneStatisticBlockService(AbstractService):
    def __init__(self, serializer_data) -> None:
        self.serializer_data = serializer_data

    def process(self):
        return {
            'zones_count': len(self.serializer_data),
            'barcodes_sum': sum([zone['barcode_amount'] for zone in self.serializer_data if zone['barcode_amount']]),
        }
