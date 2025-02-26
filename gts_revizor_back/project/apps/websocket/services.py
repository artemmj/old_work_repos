import json
from decimal import Decimal
from typing import List, Union
from uuid import UUID

from asgiref.sync import async_to_sync
from channels import layers

from api.v1.document.serializers import DocumentReadSerializer
from api.v1.zone.serializers import ZoneReadSerializer
from apps.document.models import Document
from apps.zone.models import Zone


class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, UUID):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


class SendWebSocketService:
    def __init__(self):
        self.channel_layer = layers.get_channel_layer()

    def send_about_new_zones(self, zones: List[Zone]):
        from apps.zone.managers import ZoneManager  # noqa: WPS433
        zones_ids = [zone.id for zone in zones]

        zones_filter = Zone.objects.filter(id__in=zones_ids)
        zones_with_virtual_attrs = ZoneManager().get_zones(zones_filter)

        for zone in zones_with_virtual_attrs:
            self._send_signal(serializer=ZoneReadSerializer, instance=zone, data_type='new_zone')

    def send_about_update_zones(self, zones: List[Zone]):
        from apps.zone.managers import ZoneManager  # noqa: WPS433
        zones_ids = [zone.id for zone in zones]

        zones_filter = Zone.objects.filter(id__in=zones_ids)
        zones_with_virtual_attrs = ZoneManager().get_zones(zones_filter)

        for zone in zones_with_virtual_attrs:
            self._send_signal(serializer=ZoneReadSerializer, instance=zone, data_type='update_zone')

    def send_about_delete_zones(self, zones: List[Zone]):
        from apps.zone.managers import ZoneManager  # noqa: WPS433
        zones_ids = [zone.id for zone in zones]

        zones_filter = Zone.objects.filter(id__in=zones_ids)
        zones_with_virtual_attrs = ZoneManager().get_zones(zones_filter)

        for zone in zones_with_virtual_attrs:
            self._send_signal(serializer=ZoneReadSerializer, instance=zone, data_type='delete_zone')

    def send_about_new_documents(self, documents: List[Document]):
        for document in documents:
            self._send_signal(serializer=DocumentReadSerializer, instance=document, data_type='new_document')

    def send_about_update_documents(self, documents: List[Document]):
        for document in documents:
            self._send_signal(serializer=DocumentReadSerializer, instance=document, data_type='update_document')

    def _send_signal(
        self,
        serializer: Union[ZoneReadSerializer, DocumentReadSerializer],
        instance: Union[Zone, Document],
        data_type: str,
    ):
        async_to_sync(self.channel_layer.group_send)(
            'default_room',
            {
                'type': 'send_data',
                'data': {
                    'type': data_type,
                    'data': json.loads(json.dumps(serializer(instance).data, cls=CustomJsonEncoder)),
                },
            },
        )
