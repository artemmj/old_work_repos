from typing import Dict

from constance import config
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string

from apps import app
from apps.helpers.services import AbstractService
from apps.organization.models.organization import Organization

User = get_user_model()


@app.task
def send_org_balance_email_celery_wrapper(serializer_data: Dict, user_id: str):
    return OrgBalanceEmailService(serializer_data=serializer_data, user_id=user_id).process()


class OrgBalanceEmailService(AbstractService):
    """Сервис отправки email сообщения от роута для мобилок и админки."""

    def __init__(self, serializer_data: Dict, user_id: str):  # noqa: D107
        self.organization = Organization.objects.get(pk=serializer_data.get('organization'))
        self.amount = serializer_data.get('amount')
        self.user = User.objects.get(pk=user_id)

    def process(self):
        context = {
            'amount': self.amount,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'middle_name': self.user.middle_name,
            'phone': self.user.phone,
            'organization_title': self.organization.title,
            'organization_legal_title': self.organization.legal_title,
            'organization_address': self.organization.address,
            'organization_inn': self.organization.inn,
            'organization_kpp': self.organization.kpp,
            'organization_ogrn': self.organization.ogrn,
            'organization_ogrnip': self.organization.ogrnip,
        }
        rendered = render_to_string('notifications/org_balance_email.html', context=context)
        send_mail(
            'Сформирован счет',
            rendered,
            settings.EMAIL_HOST_USER,
            [config.ORG_BALANCE_EMAIL],
            fail_silently=False,
            html_message=rendered,
        )
