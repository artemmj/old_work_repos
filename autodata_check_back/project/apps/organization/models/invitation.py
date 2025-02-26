from django.db import models
from django_lifecycle import LifecycleModelMixin, hook
from phonenumber_field.modelfields import PhoneNumberField

from apps.helpers.models import CreatedModel, UUIDModel, enum_max_length
from apps.organization.models import Membership, MembershipRoleChoices, Organization


class OrgInvitation(LifecycleModelMixin, UUIDModel, CreatedModel):
    user = models.ForeignKey(
        'user.User',
        verbose_name='Пользователь',
        related_name='org_invitations',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    phone = PhoneNumberField('Номер телефона', help_text='Пример, +79510549236')
    organization = models.ForeignKey(
        Organization,
        verbose_name='Организация',
        related_name='org_invitations',
        on_delete=models.CASCADE,
    )
    role = models.CharField(
        'Роль участника организации',
        max_length=enum_max_length(MembershipRoleChoices),
        choices=MembershipRoleChoices.choices,
    )
    is_accepted = models.NullBooleanField('Принял/Отклонил', default=None)

    class Meta:
        verbose_name = 'Приглашение на вступление в организацию'
        verbose_name_plural = 'Приглашения на вступление в организацию'

    def __str__(self):
        return f'Приглашение для {self.phone}'

    @hook('after_create')
    def after_create(self):
        from apps.organization.services import SendNotificationOrgInvitationService  # noqa: WPS433
        SendNotificationOrgInvitationService().process(self)

    @hook('after_update', when='is_accepted', has_changed=True, is_now=True)
    def add_user_to_organization(self):
        """Добавление пользователя к организации после принятия им приглашения."""
        Membership.objects.create(user=self.user, organization=self.organization, role=self.role)
