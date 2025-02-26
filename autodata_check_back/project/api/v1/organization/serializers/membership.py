from constance import config
from drf_yasg.utils import swagger_serializer_method
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from api.v1.user.serializers import UserReadSerializer
from apps.helpers.serializers import EnumField
from apps.inspection.models.inspection import Inspection
from apps.inspection_task.models.task import InspectionTask
from apps.organization.models.membership import Membership, MembershipRoleChoices
from apps.user.models import User


class MembershipReadSerializer(serializers.ModelSerializer):
    user = UserReadSerializer()
    tasks_count = serializers.SerializerMethodField()
    inspections_count = serializers.SerializerMethodField()
    self_inspection_price = serializers.SerializerMethodField()
    role = EnumField(enum_class=MembershipRoleChoices)

    class Meta:
        model = Membership
        fields = (
            'id',
            'created_at',
            'user',
            'role',
            'is_active',
            'tasks_count',
            'inspections_count',
            'self_inspection_price',
        )

    @swagger_serializer_method(serializers.IntegerField)
    def get_tasks_count(self, instance):
        return InspectionTask.objects.filter(inspector=instance.user).count()

    @swagger_serializer_method(serializers.IntegerField)
    def get_inspections_count(self, instance):
        return Inspection.objects.filter(inspector=instance.user).count()

    @swagger_serializer_method(serializers.DecimalField(max_digits=6, decimal_places=2))
    def get_self_inspection_price(self, instance):
        if instance.organization.self_inspection_price:
            return str(instance.organization.self_inspection_price)
        return str(config.SELF_INSPECTION_PRICE)


class MembershipWriteSerializer(serializers.ModelSerializer):
    phone = PhoneNumberField(required=True)
    role = serializers.ChoiceField(choices=MembershipRoleChoices.choices, required=True)

    class Meta:
        model = Membership
        fields = (
            'phone',
            'role',
        )

    def create(self, validated_data):
        new_user = User.objects.create(phone=validated_data.pop('phone'))
        new_membership = Membership.objects.create(
            user=new_user,
            organization=self.context['request'].organization,
            role=validated_data.get('role'),
        )
        return new_membership


class MembershipUpdateSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=MembershipRoleChoices.choices, required=True)

    class Meta:
        model = Membership
        fields = ('role', 'is_active')
