from dataclasses import dataclass
from typing import List, Optional, Tuple, Union
from urllib.parse import urljoin

import httpx
from django.conf import settings
from django.core.files.storage import FileSystemStorage, default_storage
from storages.backends.s3boto3 import S3Boto3StorageFile

from apps.file.models import File
from apps.helpers.services import AbstractService

FileInfo = Tuple[str, Union[FileSystemStorage, S3Boto3StorageFile], str]


@dataclass
class FaceMatchingRecognitionResponse:
    faces_is_detected: bool = False
    faces_is_equal: Optional[bool] = False
    probability: str = ''
    probability_value: Union[float, int] = 0
    result: bool = False  # noqa: WPS110
    success_call: bool = False
    error: str = ''


class FaceMatchingRecognition(AbstractService):
    """Сервис обращается в сторонний апи и возвращает процент совпадения лица на фото и в паспорте."""

    api_domain = settings.FACE_RECOGNITION_DOMAIN

    def __init__(self, image: File) -> None:
        self.url = urljoin(self.api_domain, 'verify')
        self.image = image

    def files(self) -> List[Tuple[str, FileInfo]]:
        img = default_storage.open(str(self.image.file), 'rb')
        return [('file', (str(self.image.id), img, 'image/jpeg'))]

    def process(self) -> FaceMatchingRecognitionResponse:
        try:
            response = httpx.post(url=self.url, files=self.files(), timeout=10)
            return FaceMatchingRecognitionResponse(**response.json(), success_call=True)
        except Exception as e:
            return FaceMatchingRecognitionResponse(error=str(e))
