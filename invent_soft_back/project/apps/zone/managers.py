from typing import OrderedDict

from django.db import IntegrityError, transaction
from rest_framework.exceptions import ValidationError

from apps.event.models import Event, TitleChoices
from apps.zone.models import Zone
from apps.zone.services.bulk_create import BulkCreateZoneService


class ZoneManager:

    def bulk_create(self, serializer_data: OrderedDict):
        """Создание зон в рамках конкретного проекта"""  # noqa: DAR401
        project = serializer_data['project']
        start_serial_number = serializer_data['start_serial_number']
        amount = serializer_data['amount']
        end_serial_number = amount + start_serial_number
        storage_name = serializer_data.get('storage_name')

        BulkCreateZoneService(
            project=project,
            storage_name=storage_name,
            start_serial_number=start_serial_number,
            end_serial_number=end_serial_number,
            batch_size=3000,
        ).process()

    def bulk_delete(self, serializer_data: OrderedDict):
        """Удаление зон в рамках конкретного проекта."""
        project = serializer_data['project']
        if 'zones' in serializer_data:
            zones = Zone.objects.filter(project=project, pk__in=[zone.pk for zone in serializer_data.get('zones')])
        else:
            start_serial_number = serializer_data.get('start_serial_number')
            end_serial_number = serializer_data.get('end_serial_number') + 1
            zones = Zone.objects.filter(
                project=project,
                serial_number__in=range(start_serial_number, end_serial_number),
            )

        comment = f'Удалена(ы) зона(ы) {", ".join([zone.title for zone in zones])}'
        zones.delete()
        title = TitleChoices.ZONES_DELETE
        Event.objects.create(title=title, comment=comment, project=project)
