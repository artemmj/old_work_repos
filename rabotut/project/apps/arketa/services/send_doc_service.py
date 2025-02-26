import logging
from typing import Dict

from api.v1.arketa.serializers.documents import (
    InnArketaWriteSerializer,
    RegistrationArketaWriteSerializer,
    SelfieArketaWriteSerializer,
    SnilsArketaWriteSerializer,
    SpreadArketaWriteSerializer,
)
from api.v1.file.serializers import FileSerializer
from apps.arketa.clients import ArketaFileApiClient, ArketaServiceApiClient
from apps.file.models import File
from apps.helpers.services import AbstractService

logger = logging.getLogger('django_default')


class SendDocumentToArketaService(AbstractService):

    def __init__(self, model: str, user_id: str, document_data: Dict):
        self.model = model
        self.user_id = user_id
        self.document_data = document_data
        self.serializers_map = {
            'Inn': InnArketaWriteSerializer,
            'Passport': SpreadArketaWriteSerializer,
            'Registration': RegistrationArketaWriteSerializer,
            'Selfie': SelfieArketaWriteSerializer,
            'Snils': SnilsArketaWriteSerializer,
        }
        self.api_client_methods_map = {
            'Inn': 'put_inn',
            'Passport': 'put_spread',
            'Registration': 'put_registration',
            'Selfie': 'put_selfie',
            'Snils': 'put_snils',
        }

    def upload_file_to_arketa(self, file_id: str):
        db_file = File.objects.get(pk=file_id)
        arketa_file_data = ArketaFileApiClient().create_file(FileSerializer(db_file).data)
        return arketa_file_data.get('id')

    def load_files(self):
        if self.model == 'Selfie':
            return self.upload_file_to_arketa()
        elif self.model == 'Registration':
            return [self.upload_file_to_arketa(fid) for fid in self.document_data]

    def process(self, *args, **kwargs):
        serializer = self.serializers_map.get(self.model)(data=self.document_data)
        serializer.is_valid(raise_exception=True)
        method = self.api_client_methods_map.get(self.model)
        serializer_data = serializer.data
        files_ids = self.load_files()
        if files_ids:
            serializer_data['file'] = files_ids
        return getattr(ArketaServiceApiClient(), method)(user_id=self.user_id, payload=serializer_data)
