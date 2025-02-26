import logging

from constance import config
from django.db import models
from django_lifecycle import LifecycleModelMixin, hook

from apps.devices.tasks import send_push
from apps.helpers.models import CreatedModel, UUIDModel, enum_max_length
from apps.notification.models import TemplateInvitationNotification
from apps.organization.models.membership import Membership
from apps.template.models import Template

logger = logging.getLogger('django')


class TemplateInvitationStatuses(models.TextChoices):
    ACCEPTED = ('accepted', 'Принято')
    CANCELED = ('canceled', 'Отменено')
    PENDING = ('pending', 'В ожидании')


class TemplateInvitation(LifecycleModelMixin, UUIDModel, CreatedModel):
    user = models.ForeignKey(
        'user.User',
        verbose_name='приглашаемый пользователь',
        related_name='template_invitations',
        on_delete=models.CASCADE,
    )
    template = models.ForeignKey(
        Template,
        verbose_name='Шаблон',
        related_name='template_invitations',
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        'Статус',
        max_length=enum_max_length(TemplateInvitationStatuses),
        choices=TemplateInvitationStatuses.choices,
        default=TemplateInvitationStatuses.PENDING,
    )

    class Meta:
        verbose_name = 'Приглашение принять шаблон'
        verbose_name_plural = 'Приглашения принять шаблон'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'template', 'status'],
                name='Приглашение принять шаблон без ответа',
                condition=models.Q(status=TemplateInvitationStatuses.PENDING),
            ),
        ]

    def __str__(self):
        return f'Приглашение для {self.user.phone}'  # noqa: WPS237

    @hook('after_create')
    def send_notification(self):  # noqa: WPS210
        """Уведомление после создания приглашения принять."""
        user_l_name = self.template.user.last_name
        user_f_name = self.template.user.first_name
        message = config.SHARE_TEMPLATE.replace('[ ]', f'{user_f_name} {user_l_name}')

        membership = Membership.objects.filter(user=self.user, is_active=True)
        user_pk = self.user.pk
        if not membership:
            logger.error(
                f'Не найдена активная организация пользователя {user_pk} ',
                'при создании уведомления о принятии шаблона',
            )
            return
        if membership.count() > 1:
            logger.error(f'Внимание, ошибка: за пользователем {user_pk} более одной активной организации!')
            return

        organization = membership[0].organization
        message += f'\r\n\r\nОрганизация: {organization.title}'  # noqa: WPS336
        message += f'\r\nШаблон: {self.template.title}'  # noqa: WPS237 WPS336

        notification = TemplateInvitationNotification.objects.create(
            user=self.user,
            message=message,
            template_invitation=self,
            organization=organization,
        )
        send_push.delay(
            str(self.user_id),
            message,
            {
                'push_type': 'TemplateInvitationNotification',
                'template_invitation': str(self.id),
                'notification_id': str(notification.id),
            },
        )

    @hook(
        'after_update',
        when='status',
        was=TemplateInvitationStatuses.PENDING,
        is_now=TemplateInvitationStatuses.ACCEPTED,
    )
    def create_template_after_accepted(self):
        from apps.template.services import CreateTemplateService  # noqa: WPS433
        CreateTemplateService(user_id=self.user_id, template=self.template).process()
