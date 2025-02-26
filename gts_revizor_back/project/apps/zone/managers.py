from typing import OrderedDict

from django.db import IntegrityError
from django.db.models import QuerySet

from apps.event.models import Event, TitleChoices
from apps.websocket.services import SendWebSocketService
from apps.zone.models import Zone
from apps.zone.services.check_for_documents_in_zones import CheckForDocumentsInZonesService


class ZoneManager:

    def bulk_create(self, serializer_data: OrderedDict):
        """Создание зон в рамках конкретного проекта"""  # noqa: DAR401
        project = serializer_data['project']
        start_serial_number = serializer_data['start_serial_number']
        amount = serializer_data['amount']
        end_serial_number = amount + start_serial_number
        storage_name = serializer_data.get('storage_name')

        new_zones = []
        for idx, number in enumerate(range(start_serial_number, end_serial_number)):
            try:
                zone = Zone.objects.create(
                    project=project,
                    serial_number=number,
                    code=number,
                    storage_name=storage_name,
                    title=f'Зона {number}',
                )
            except IntegrityError:
                continue
            if idx < 100:
                new_zones.append(zone)

        # Отослать сигналы только по первым 100 зонам.
        SendWebSocketService().send_about_new_zones(zones=new_zones)

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

        CheckForDocumentsInZonesService(zones=zones).process()

        zones = zones.order_by('serial_number')
        SendWebSocketService().send_about_delete_zones(zones=zones[:100])
        comment = f'Удалены зоны с {zones.first().serial_number} по {zones.last().serial_number}'
        zones.delete()
        title = TitleChoices.ZONES_DELETE
        Event.objects.create(title=title, comment=comment, project=project)

    def get_zones(self, queryset: QuerySet) -> QuerySet:
        """Получение зон с дополнительными атрибутами."""
        return (
            queryset
            .calculate_barcode_amount()
            .calculate_tasks_scanned_products_count()
            .get_counter_scan_tasks()
            .get_counter_scan_tasks_status()
            .get_controller_tasks()
            .get_controller_tasks_status()
            .get_auditor_tasks()
            .get_auditor_tasks_status()
            .get_auditor_controller_tasks()
            .get_auditor_controller_tasks_status()
            .get_auditor_external_controller_tasks()
            .get_auditor_external_controller_tasks_status()
            .get_storage_tasks()
            .get_storage_tasks_status()
        )
