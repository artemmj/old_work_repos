import json
import os
import pathlib
import zipfile

from rest_framework.exceptions import ValidationError

from apps.file.models import File
from apps.helpers.services import AbstractService


class UnzipService(AbstractService):
    """Сервис проверки и открытия zip файла."""

    def __init__(self, file_id: str):
        self.file = File.objects.get(pk=file_id)

    def process(self):
        self._validated_file_extension()

        dir_path = os.path.splitext(self.file.file.path)[0]
        os.makedirs(dir_path, exist_ok=True)

        zipped_file = zipfile.ZipFile(self.file.file.path)
        for zip_file in zipped_file.namelist():
            zipped_file.extract(zip_file, dir_path)

        with open(f'{dir_path}/data.json') as f:
            return json.load(f)

    def _validated_file_extension(self):
        file_extension = pathlib.Path(self.file.file.url).suffix
        if file_extension != '.zip':
            raise ValidationError('Для загрузки необходим файл формата zip.')
