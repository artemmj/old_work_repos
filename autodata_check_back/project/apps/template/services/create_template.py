import json

from apps.helpers.services import AbstractService
from apps.organization.models.membership import Membership


class CreateTemplateService(AbstractService):
    """Сервис создания шаблона."""

    def __init__(self, user_id, template=None):  # noqa: D107
        self.user_id = user_id
        self.template = template

    def process(self):  # noqa: WPS210
        from api.v1.template.serializers.template import ForCreateTemplateServiceSerializer  # noqa: WPS433

        if self.template:
            json_data = ForCreateTemplateServiceSerializer(self.template).data
            json_data['is_active'] = False
        else:
            with open('/app/apps/template/assets/default_template_data.json') as f:
                json_data = json.load(f)

        json_data['user'] = str(self.user_id)
        serializer = ForCreateTemplateServiceSerializer(data=json_data)
        serializer.is_valid(raise_exception=True)
        template = serializer.save()

        membership = Membership.objects.filter(user=template.user, is_active=True).first()
        if membership:
            title = json_data.get('title')
            org_title = membership.organization.title
            json_data['title'] = f'{title}, {org_title}'
