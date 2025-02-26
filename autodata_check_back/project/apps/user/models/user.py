from typing import Final, final

from django.contrib.auth import models as auth_models
from django.db import models
from django_lifecycle import LifecycleModelMixin, hook
from phonenumber_field.modelfields import PhoneNumberField

import settings
from apps.file.models import Image
from apps.helpers.managers import CustomFieldUserManager
from apps.helpers.model_fields import ChoiceArrayField
from apps.helpers.models import CreatedModel, UUIDModel, enum_max_length
from apps.organization.models import Membership, MembershipRoleChoices, Organization, OrgInvitation
from apps.template.services import CreateTemplateService

_FIELD_MAX_LENGTH: Final = 40


class RoleChoices(models.TextChoices):
    CUSTOMER = 'customer', 'Заказчик'    # noqa: WPS115
    INSPECTOR = 'inspector', 'Инспектор'    # noqa: WPS115
    DISPATCHER = 'dispatcher', 'Диспетчер'    # noqa: WPS115
    ADMINISTRATOR = 'administrator', 'Администратор'    # noqa: WPS115


def get_default_role():
    return [RoleChoices.CUSTOMER]


@final
class User(LifecycleModelMixin, UUIDModel, auth_models.AbstractUser, CreatedModel):
    username = models.CharField('Имя пользователя', max_length=_FIELD_MAX_LENGTH, default='', blank=True)
    first_name = models.CharField('Имя', max_length=_FIELD_MAX_LENGTH)
    middle_name = models.CharField('Отчество', max_length=_FIELD_MAX_LENGTH, default='', blank=True)
    last_name = models.CharField('Фамилия', max_length=_FIELD_MAX_LENGTH)
    phone = PhoneNumberField('Номер телефона', unique=True, help_text='Пример, +79510549236')
    email = models.EmailField('Адрес электронной почты', default='', null=True, blank=True)
    avatar = models.ForeignKey(
        Image,
        verbose_name='Аватар',
        related_name='users',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    agreement_policy = models.BooleanField(
        verbose_name='Согласие с условиями политики конфиденциальности',
        default=False,
    )
    agreement_processing = models.BooleanField(
        verbose_name='Согласие на обработку персональных данных',
        default=False,
    )
    roles = ChoiceArrayField(
        models.CharField(
            'Роль',
            max_length=enum_max_length(RoleChoices),
            choices=RoleChoices.choices,
            default=RoleChoices.CUSTOMER,
        ),
        verbose_name='Роли',
        default=get_default_role,
    )

    objects = CustomFieldUserManager(username_field_name='phone')  # noqa: WPS110

    USERNAME_FIELD = 'phone'    # noqa: WPS115
    REQUIRED_FIELDS = ('first_name', 'last_name', 'email')    # noqa: WPS115

    class Meta(auth_models.AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        ordering = ('email',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_username(self):
        # for jwt_payload_handler
        return str(self.phone)

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    def create_organization(self) -> Organization:
        """Создание организации после регистрации пользователя."""
        return Organization.objects.create(
            title=f'{self.last_name} {self.first_name} {self.middle_name}',
        )

    def create_memberships_and_accept_invitations(self, organization: Organization):
        """Добавление пользователя в организации и принятие приглашений на вступление после регистрации."""
        org_invitations = OrgInvitation.objects.filter(user__isnull=True, phone=self.phone, is_accepted__isnull=True)
        memberships = [
            Membership(user_id=self.pk, organization_id=inv.organization_id, role=inv.role)
            for inv in org_invitations
        ]
        memberships.append(Membership(
            user=self, organization=organization, role=MembershipRoleChoices.OWNER, is_active=True,
        ))
        Membership.objects.bulk_create(memberships)
        org_invitations.update(is_accepted=True)

    @hook('after_create')
    def after_create(self):
        organization = self.create_organization()
        self.create_memberships_and_accept_invitations(organization)
        CreateTemplateService(self.pk).process()

    @hook('before_delete')
    def before_delete(self):
        remote_user = User.objects.filter(phone=settings.REMOTE_USER_PHONE).first()
        self.inspections.update(inspector=remote_user)
        self.author_inspection_tasks.update(author=remote_user)
        self.inspector_inspection_tasks.update(inspector=remote_user)
        self.transactions.update(user=remote_user)
