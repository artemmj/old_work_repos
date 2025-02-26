from typing import Dict

from constance import config
from rest_framework.exceptions import ValidationError

from apps.helpers.services import AbstractService


class ValidateInspectionsAttrService(AbstractService):
    """Сервис проверяет поля inspection и accreditation_inspection в осмотре."""

    def __init__(self, attrs: Dict):  # noqa: D107
        self.attrs = attrs

    def process(self):
        if 'inspection' in self.attrs and 'accreditation_inspection' in self.attrs:
            if self.attrs.get('inspection') and self.attrs.get('accreditation_inspection'):
                raise ValidationError({
                    'inspection': config.INSPECTION_NEED_NULL_VALUE_ERROR,
                    'accreditation_inspection': config.INSPECTION_NEED_NULL_VALUE_ERROR,
                })
