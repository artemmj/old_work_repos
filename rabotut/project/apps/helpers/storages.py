import io
import os
from pathlib import Path

import requests
from django.core.files import File as FileObject
from storages.backends.s3boto3 import S3Boto3Storage

from apps.file.models import File


class MediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = True


def download_file(file_url: str) -> bytes:
    """Получение байткода файла из s3."""
    try:
        return requests.get(file_url, timeout=30).content  # noqa: WPS432
    except requests.exceptions.RequestException:
        return b''


def save_file_to_db(file_path: str) -> str:
    """Сохраняет файл в базу данных.

    Args:
        file_path: путь к сохраняемому файлу

    Returns:
        str: ссылка на сохранённый файл
    """
    file_name = Path(file_path).name

    with open(file_path, 'rb') as f:
        file_obj = FileObject(io.BytesIO(f.read()), name=file_name)
        file_in_db = File.objects.create(file=file_obj)
    if os.path.isfile(file_name):
        os.remove(file_name)
    if os.path.isfile(file_path):
        os.remove(file_path)
    return file_in_db.file.url
