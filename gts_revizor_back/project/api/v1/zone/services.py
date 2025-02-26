from typing import Dict

from django.db.models import Prefetch
from rest_framework.exceptions import ValidationError

from apps.helpers.services import AbstractService
from apps.product.models import AdditionalProductTitleAttribute
from apps.project.models import Project
from apps.zone.models import Zone

from .serializers import ZoneWriteSerializer


class ZoneStatisticBlockService(AbstractService):
    def __init__(self, serializer_data) -> None:
        self.serializer_data = serializer_data

    def process(self):
        return {
            'zones_count': len(self.serializer_data),
            'barcodes_sum': sum([zone['barcode_amount'] for zone in self.serializer_data if zone['barcode_amount']]),
        }


def bulk_update_zones(serializer_data: dict):  # noqa: WPS231 DAR401
    """Функция выполняет адпейт пачки зон, либо по айди зон, либо по айди проекта + serial_number."""  # noqa: DAR401
    return_data = []

    for update_data in serializer_data:
        if 'id' in update_data and 'project_id' not in update_data and 'serial_number' not in update_data:
            # Апдейтим по айди зоны
            zone = Zone.objects.get(pk=update_data.get('id'))
        elif 'project_id' in update_data and 'serial_number' in update_data:
            # Апдейтим по проекту и порядковому номеру зоны
            project = Project.objects.get(pk=update_data.get('project_id'))
            zone = Zone.objects.get(project=project, serial_number=update_data.get('serial_number'))
        else:
            raise ValidationError('Возникла непредвиденная ошибка.')

        serializer = ZoneWriteSerializer(zone, data=update_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return_data.append(serializer.data)

    return return_data


class GetZoneTasksService(AbstractService):
    """Сервис для получения заданий зоны."""

    def __init__(self, zone: Zone, tasks_filter_params: Dict) -> None:
        self.zone = zone
        self.tasks_filter_params = tasks_filter_params

    def process(self):
        return (
            self.zone
            .tasks
            .filter(**self.tasks_filter_params)
            .prefetch_related(
                'scanned_products__product',
                Prefetch(
                    'scanned_products__product__title_attrs',
                    queryset=AdditionalProductTitleAttribute.objects.filter(is_hidden=False).only('content'),
                    to_attr='additional_title_attrs',
                ),
                Prefetch(
                    'scanned_products__product__title_attrs',
                    queryset=AdditionalProductTitleAttribute.objects.filter(is_hidden=True).only('content'),
                    to_attr='hide_title_attrs',
                ),
            )
        )
