from constance import config
from rest_framework.exceptions import ValidationError

from apps.helpers.services import AbstractService
from apps.inspector.models import Inspector
from apps.user.models import RoleChoices


class AccreditationCreateInspectorService(AbstractService):
    """Сервис создает и закрепляет за юзером инспектора, когда успешно прошли аккредитацию."""

    def __init__(self, instance):  # noqa: D107
        self.instance = instance
        self.user = instance.user

    def process(self):
        if self.user.inspectors.exists():
            raise ValidationError({'inspectors': config.ACCRED_USER_ALREADY_INSPECTOR_ERROR.replace('USER', self.user)})

        Inspector.objects.create(
            inn=self.instance.inn,
            work_skills=self.instance.work_skills,
            availability_thickness_gauge=self.instance.availability_thickness_gauge,
            city=self.instance.city,
            radius=self.instance.radius,
            user=self.user,
        )

        self.user.roles.append(RoleChoices.INSPECTOR)
        self.user.save()
