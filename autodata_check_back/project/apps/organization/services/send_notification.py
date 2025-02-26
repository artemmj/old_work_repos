from constance import config

from apps.devices.tasks import send_push
from apps.helpers.services import AbstractService
from apps.helpers.sms import SmsAPI
from apps.notification.models import OrganizationInvitationNotification
from apps.organization.models import OrgInvitation


class SendNotificationOrgInvitationService(AbstractService):
    """Сервис отправки пользователю смс или пуша о приглашении в организацию."""

    def process(self, org_invitation: OrgInvitation):
        if not org_invitation.user:  # noqa: WPS504
            msg_one = 'Вы получили приглашение в организацию '
            msg_two = ', скачайте приложение Автодата Автоинспектор и зарегистрируйтесь.'
            sms_text = f'{msg_one}{org_invitation.organization.title}{msg_two}'  # noqa: WPS237
            SmsAPI().send_sms(sms_text, str(org_invitation.phone))
        else:
            message = config.INVITE_ORGANIZATION.replace('[ ]', org_invitation.organization.title)
            message += f'\r\n\r\nОрганизация: {org_invitation.organization.title}'  # noqa: WPS237 WPS336

            notification = OrganizationInvitationNotification.objects.create(
                user=org_invitation.user,
                message=message,
                org_invitation=org_invitation,
            )
            send_push.delay(
                str(org_invitation.user_id),
                message,
                {
                    'push_type': 'OrganizationInvitationNotification',
                    'org_invitation': str(org_invitation.id),
                    'notification_id': str(notification.id),
                },
            )
