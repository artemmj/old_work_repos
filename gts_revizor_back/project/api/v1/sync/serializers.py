from rest_framework import serializers

from api.v1.employee.serializers import EmployeeWideSerializer
from api.v1.project.serializers.rmm_settings import RMMSettingsReadSerializer
from api.v1.project.serializers.terminal_settings import TerminalSettingsReadSerializer
from api.v1.user.serializers import UserReadSerializer
from apps.employee.models import Employee
from apps.project.models import Project
from apps.task.models import Task
from apps.terminal.models import Terminal
from apps.zone.models import Zone


class GetProjectDataRequestSerializer(serializers.Serializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), required=True)


class GetProjectDataResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    created_at = serializers.DateTimeField()
    title = serializers.CharField()
    address = serializers.CharField()
    manager = UserReadSerializer()
    rmm_settings = RMMSettingsReadSerializer()
    terminal_settings = TerminalSettingsReadSerializer()
    employees = EmployeeWideSerializer(many=True)


class SendOfflineDataSerializer(serializers.Serializer):

    class SendOfflineDataUsersSerializer(serializers.Serializer):  # noqa: WPS431

        class TasksSerializer(serializers.Serializer):  # noqa: WPS431

            class ScanProductSerializer(serializers.Serializer):  # noqa: WPS431
                product = serializers.CharField(required=True)
                amount = serializers.IntegerField(required=True)
                scanned_time = serializers.DateTimeField(required=False)
                is_weight_product = serializers.BooleanField(required=True)
                added_by_product_code = serializers.BooleanField(required=False)
                added_by_qr_code = serializers.BooleanField(required=False)
                dm = serializers.CharField(required=False)
                title = serializers.CharField(required=False)
                vendor_code = serializers.CharField(required=False)
                qr_code = serializers.CharField(required=False)

            class DocumentSerializer(serializers.Serializer):  # noqa: WPS431
                zone = serializers.PrimaryKeyRelatedField(queryset=Zone.objects.all())
                employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
                start_audit_date = serializers.DateTimeField(required=False)
                end_audit_date = serializers.DateTimeField(required=True)
                tsd_number = serializers.IntegerField(required=True)

            id = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(), required=True)
            scanned_products = ScanProductSerializer(many=True, required=False)
            document = DocumentSerializer(required=True)
            result = serializers.FloatField(required=False)

        id = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), required=True)
        tasks = serializers.ListField(child=TasksSerializer(), required=True, allow_empty=False)

    terminal = serializers.PrimaryKeyRelatedField(queryset=Terminal.objects.all(), required=True)
    terminal_time = serializers.DateTimeField(required=True)
    users = serializers.ListField(child=SendOfflineDataUsersSerializer(), allow_empty=False)
