from constance import config
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.v1.template.serializers.template import TemplateShortSerializer
from apps.helpers.serializers import EnumField
from apps.organization.models import Organization
from apps.template.models import Template, TemplateInvitation, TemplateInvitationStatuses

User = get_user_model()


class TemplateInvitationReadSerializer(serializers.ModelSerializer):
    template = TemplateShortSerializer()
    status = EnumField(enum_class=TemplateInvitationStatuses)

    class Meta:
        model = TemplateInvitation
        fields = ('id', 'created_at', 'template', 'status')


class TemplateInvitationCreateByPhoneSerializer(serializers.Serializer):
    phone = PhoneNumberField(required=True)
    template = serializers.PrimaryKeyRelatedField(queryset=Template.objects.all())

    def validate(self, attrs):
        if TemplateInvitation.objects.filter(  # noqa: WPS337
            user__phone=attrs['phone'],
            template=attrs['template'],
            status=TemplateInvitationStatuses.PENDING,
        ).exists():
            raise ValidationError({'error': config.TEMPLATE_INVITATION_ALREADY_HAVE_ERROR})
        return attrs

    def create(self, validated_data):
        phone = validated_data.pop('phone')
        user = get_object_or_404(User, phone=phone)
        validated_data['user'] = user
        instance = TemplateInvitation.objects.create(**validated_data)
        return instance


class TemplateInvitationCreateByOrganizationSerializer(serializers.Serializer):  # noqa: WPS118
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all())
    template = serializers.PrimaryKeyRelatedField(queryset=Template.objects.all())
