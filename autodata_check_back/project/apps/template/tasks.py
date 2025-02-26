import logging
from uuid import UUID

from django.db import IntegrityError

from apps import app
from apps.organization.models import Organization
from apps.template.models import TemplateInvitation

logger = logging.getLogger('django')


@app.task
def create_template_invitation_task(organization_id: UUID, template_id: UUID, owner_id: UUID):
    organization = Organization.objects.get(id=organization_id)
    org_users = organization.users.exclude(id=owner_id)

    for user in org_users:
        try:
            TemplateInvitation.objects.create(user=user, template_id=template_id)
        except IntegrityError as exc:
            logger.error(f'Возникла ошибка, при создании приглашения принять шаблон, пропускаю ... {exc}')
