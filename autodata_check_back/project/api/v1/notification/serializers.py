from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer

from apps.helpers.serializers import EnumField
from apps.notification.models import (  # noqa: WPS235
    BaseNotification,
    CantGetTaskWithoutRequisiteNotification,
    InspectorAccrNewFixesNotification,
    InspectorAccrSuccCompleteNotification,
    InspectorAddBalanceNotification,
    IssuingOrganizationInspectorNotification,
    IssuingServiceInspectorNotification,
    NotificationStatuses,
    OrganizationAddBalanceNotification,
    OrganizationInvitationNotification,
    TaskAcceptedNotification,
    TaskCompletedNotification,
    TaskFixOrganizationInspectorNotification,
    TaskFixServiceInspectorNotification,
    TaskInvitationNotification,
    TemplateInvitationNotification,
)
from apps.organization.models.organization import Organization


class BaseNotificationSerializer(serializers.ModelSerializer):
    status = EnumField(enum_class=NotificationStatuses)

    class Meta:
        model = BaseNotification
        fields = ('id', 'created_at', 'message', 'status')
        read_only_fields = ('id', 'created_at')


class InspectorAddBalanceNotificationSerializer(BaseNotificationSerializer):
    class Meta:
        model = InspectorAddBalanceNotification
        fields = ('id', 'created_at', 'message', 'status')


class IssuingOrganizationInspectorNotificationSerializer(BaseNotificationSerializer):  # noqa: WPS118
    class Meta:
        model = IssuingOrganizationInspectorNotification
        fields = ('id', 'created_at', 'message', 'status')


class IssuingServiceInspectorNotificationSerializer(BaseNotificationSerializer):
    class Meta:
        model = IssuingServiceInspectorNotification
        fields = ('id', 'created_at', 'message', 'status')


class OrganizationAddBalanceNotificationSerializer(BaseNotificationSerializer):
    class Meta:
        model = OrganizationAddBalanceNotification
        fields = ('id', 'created_at', 'message', 'status')


class OrganizationInvitationNotificationSerializer(BaseNotificationSerializer):
    class Meta:
        model = OrganizationInvitationNotification
        fields = ('id', 'created_at', 'message', 'status', 'org_invitation')


class TaskAcceptedNotificationSerializer(BaseNotificationSerializer):
    class Meta:
        model = TaskAcceptedNotification
        fields = ('id', 'created_at', 'message', 'status', 'inspection_task')


class TaskCompletedNotificationSerializer(BaseNotificationSerializer):
    class Meta:
        model = TaskCompletedNotification
        fields = ('id', 'created_at', 'message', 'status', 'inspection_task')


class TaskFixOrganizationInspectorNotificationSerializer(BaseNotificationSerializer):  # noqa: WPS118
    class Meta:
        model = TaskFixOrganizationInspectorNotification
        fields = ('id', 'created_at', 'message', 'status', 'inspection_task')


class TaskFixServiceInspectorNotificationSerializer(BaseNotificationSerializer):
    class Meta:
        model = TaskFixServiceInspectorNotification
        fields = ('id', 'created_at', 'message', 'status', 'inspection_task')


class TaskInvitationNotificationSerializer(BaseNotificationSerializer):
    class Meta:
        model = TaskInvitationNotification
        fields = ('id', 'created_at', 'message', 'status', 'inspection_task_invitation')


class TemplateInvitationNotificationSerializer(BaseNotificationSerializer):
    class Meta:
        model = TemplateInvitationNotification
        fields = ('id', 'created_at', 'message', 'status', 'template_invitation')


class AccrNewFixesNotificationSerializer(BaseNotificationSerializer):
    class Meta:
        model = InspectorAccrNewFixesNotification
        fields = ('id', 'created_at', 'message', 'status', 'accreditation_inspection')


class AccrSuccCompleteNotificationSerializer(BaseNotificationSerializer):
    class Meta:
        model = InspectorAccrSuccCompleteNotification
        fields = ('id', 'created_at', 'message', 'status', 'accreditation_inspection')


class CantGetTaskWithoutRequisiteNotificationSerializer(BaseNotificationSerializer):  # noqa: WPS118
    class Meta:
        model = InspectorAccrSuccCompleteNotification
        fields = ('id', 'created_at', 'message', 'status')


class NotificationPolymorphicSerializer(PolymorphicSerializer):
    base_serializer_class = BaseNotificationSerializer
    model_serializer_mapping = {
        InspectorAddBalanceNotification: InspectorAddBalanceNotificationSerializer,
        IssuingOrganizationInspectorNotification: IssuingOrganizationInspectorNotificationSerializer,
        IssuingServiceInspectorNotification: IssuingServiceInspectorNotificationSerializer,
        OrganizationAddBalanceNotification: OrganizationAddBalanceNotificationSerializer,
        OrganizationInvitationNotification: OrganizationInvitationNotificationSerializer,
        TaskAcceptedNotification: TaskAcceptedNotificationSerializer,
        TaskCompletedNotification: TaskCompletedNotificationSerializer,
        TaskFixOrganizationInspectorNotification: TaskFixOrganizationInspectorNotificationSerializer,
        TaskFixServiceInspectorNotification: TaskFixServiceInspectorNotificationSerializer,
        TaskInvitationNotification: TaskInvitationNotificationSerializer,
        TemplateInvitationNotification: TemplateInvitationNotificationSerializer,
        InspectorAccrNewFixesNotification: AccrNewFixesNotificationSerializer,
        InspectorAccrSuccCompleteNotification: AccrSuccCompleteNotificationSerializer,
        CantGetTaskWithoutRequisiteNotification: CantGetTaskWithoutRequisiteNotificationSerializer,
    }


class CarsInfoSerializer(serializers.Serializer):
    organization = serializers.UUIDField()
    inspection = serializers.UUIDField()
    task = serializers.UUIDField()
    template = serializers.CharField()
    brand = serializers.CharField()
    model = serializers.CharField()
    vin_code = serializers.CharField()
    planned_date = serializers.DateTimeField()


class NotificationResponseSwaggerSerializer(serializers.ModelSerializer):
    inspection_task = serializers.UUIDField(required=False)
    inspection_task_invitation = serializers.UUIDField(required=False)
    org_invitation = serializers.UUIDField(required=False)
    template_invitation = serializers.UUIDField(required=False)
    accreditation_inspection = serializers.UUIDField(required=False)
    status = EnumField(enum_class=NotificationStatuses)
    organization = serializers.CharField()
    cars_info = CarsInfoSerializer(many=True)
    resourcetype = serializers.ChoiceField(
        choices=(  # noqa: WPS317
            'TaskInvitationNotification', 'TaskAcceptedNotification', 'TaskCompletedNotification',
            'TaskFixOrganizationInspectorNotification', 'TaskFixServiceInspectorNotification',
            'InspectorAddBalanceNotification', 'IssuingOrganizationInspectorNotification',
            'TemplateInvitationNotification', 'OrganizationInvitationNotification',
            'OrganizationAddBalanceNotification', 'InspectorAccrNewFixesNotification',
            'InspectorAccrSuccCompleteNotification', 'CantGetTaskWithoutRequisiteNotification',
            'IssuingServiceInspectorNotification',
        ),
        required=True,
    )

    class Meta:
        model = BaseNotification
        fields = (
            'id',
            'created_at',
            'message',
            'status',
            'inspection_task',
            'inspection_task_invitation',
            'org_invitation',
            'template_invitation',
            'resourcetype',
            'accreditation_inspection',
            'organization',
            'cars_info',
        )
        read_only_fields = ('id', 'created_at')


class NotificationNewCountSerializer(serializers.Serializer):
    new_count = serializers.IntegerField(help_text='Кол-во новых уведомлений')


class NotificationViewedSerializer(serializers.Serializer):
    notifications = serializers.PrimaryKeyRelatedField(
        queryset=BaseNotification.objects.all(), many=True, required=True,
    )


class SendOrgBalanceEmailSerializer(serializers.Serializer):
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all())
    amount = serializers.DecimalField(max_digits=19, decimal_places=2)  # noqa: WPS432
