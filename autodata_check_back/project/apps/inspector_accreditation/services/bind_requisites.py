from typing import Dict

from constance import config
from rest_framework.exceptions import ValidationError

from apps.helpers.services import AbstractService
from apps.inspector.models import Requisite
from apps.user.models import User


class BindRequisiteService(AbstractService):
    """Сервис по привязке реквизитов к инспектору."""

    def __init__(self, user: User, serializer_data: Dict):  # noqa: D107
        self.user = user
        self.serializer_data = serializer_data

    def process(self):
        if not self.user.inspectors.all():
            raise ValidationError({
                'inspectors': config.BIND_REQUISITES_USER_IS_NOT_INSPECTOR_ERROR.replace('USER', self.user),
            })

        if hasattr(self.user.inspectors.first(), 'requisite'):  # noqa: WPS421
            raise ValidationError({
                'requisites': config.BIND_REQUISITES_USER_ALREADY_HAVE_REQUISITES_ERROR.replace('USER', self.user),
            })

        self.serializer_data['inspector'] = self.user.inspectors.first()
        Requisite.objects.create(**self.serializer_data)
