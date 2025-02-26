from constance import config
from django.contrib.auth import get_user_model
from django.db.models import Q  # noqa: WPS347
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.helpers.serializers import EagerLoadingSerializerMixin, EnumField
from apps.organization.models import Membership, MembershipRoleChoices, OrgInvitation

User = get_user_model()


class OrgInvitationReadSerializer(EagerLoadingSerializerMixin, serializers.ModelSerializer):
    organization = serializers.CharField(source='organization.title')
    role = EnumField(enum_class=MembershipRoleChoices)

    select_related_fields = ('organization',)

    class Meta:
        model = OrgInvitation
        fields = ('id', 'created_at', 'phone', 'organization', 'role', 'is_accepted')


class OrgInvitationWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrgInvitation
        fields = ('id', 'phone', 'organization', 'role', 'is_accepted')

    def validate(self, attrs):
        phone = attrs['phone']
        organization = attrs['organization']
        if Membership.objects.filter(user__phone=phone, organization=organization).exists():
            raise ValidationError({
                'error': config.ORG_INVITATION_USER_IS_MEMBERSHIP_ERROR.replace('PHONE', str(phone)),
            })
        if OrgInvitation.objects.filter(  # noqa: WPS337
            Q(user__phone=phone) | Q(phone=phone), organization=organization, is_accepted__isnull=True,
        ).exists():
            raise ValidationError({
                'error': config.ORG_INVITATION_USER_HAVE_INVITE_ERROR.replace('PHONE', str(phone)),
            })
        return attrs

    def create(self, validated_data):
        phone = validated_data['phone']
        if User.objects.filter(phone=phone).exists():
            validated_data['user'] = User.objects.get(phone=phone)
        return super().create(validated_data)
