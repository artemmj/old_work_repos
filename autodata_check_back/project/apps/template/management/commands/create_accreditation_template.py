import json

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand, CommandError

from api.v1.template.serializers.template import ForCreateTemplateServiceSerializer
from apps.template.models import Template

User = get_user_model()


class Command(BaseCommand):
    help = 'Создание шаблона для аккредитации'

    def handle(self, *args, **kwargs):  # noqa: WPS110
        if not Template.objects.filter(is_accreditation=True).exists():  # noqa: WPS504
            user = User.objects.filter(is_superuser=True).first()
            with open('/app/apps/template/assets/accreditation_template_data.json') as f:
                json_data = json.load(f)
                json_data['user'] = str(user.pk)
                serializer = ForCreateTemplateServiceSerializer(data=json_data)
                serializer.is_valid(raise_exception=True)
            try:  # noqa: WPS229
                serializer.save()
                print('Создание шаблона для аккредитации завершилось успешно.')  # noqa: T001, WPS421, T201
            except Exception as e:
                raise CommandError(e)
        else:
            raise CommandError('Шаблон для аккредитации уже создан.')
