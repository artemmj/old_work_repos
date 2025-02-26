from rest_framework import serializers

from apps.document.models import Document
from apps.employee.models import Employee
from apps.event.models import Event
from apps.product.models import Product, ScannedProduct
from apps.project.models import Project
from apps.project.models.rmm_settings import RMMSettings
from apps.project.models.terminal_settings import TerminalSettings
from apps.task.models import Task
from apps.terminal.models import Terminal
from apps.user.models import User
from apps.zone.models import Zone


class ProjectBackupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('title', 'created_at', 'address')


class TerminalSettingsBackupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TerminalSettings
        fields = (
            'issuing_task',
            'length_barcode_pallets',
            'error_correction',
            'compliance_codes',
            'product_name',
            'unknown_barcode',
            'trimming_barcode',
            'recalculation_discrepancy',
            'suspicious_barcodes_amount',
            'check_dm',
            'check_am',
            'search_by_product_code',
            'manual_input_quantity',
        )


class RMMSettingsBackupSerializer(serializers.ModelSerializer):
    class Meta:
        model = RMMSettings
        fields = ('auto_zones_amount', 'password', 'norm', 'extended_tasks')


class EmployeeBackupSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='pk')

    class Meta:
        model = Employee
        fields = ('id', 'serial_number', 'username', 'roles', 'is_deleted')


class TerminalBackupSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='pk')

    class Meta:
        model = Terminal
        fields = ('id', 'number', 'ip_address', 'db_loading', 'last_connect')


class ProductBackupSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='pk')

    class Meta:
        model = Product
        fields = (
            'id',
            'vendor_code',
            'barcode',
            'title',
            'remainder',
            'remainder_2',
            'size',
            'price',
            'am',
            'dm',
            'qr_code',
        )


class ScannedProductSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='product.pk')

    class Meta:
        model = ScannedProduct
        fields = (
            'created_at',
            'scanned_time',
            'product',
            'amount',
            'added_by_product_code',
            'added_by_qr_code',
        )


class TaskReadSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='pk')
    scanned_products = ScannedProductSerializer(many=True)
    employee = serializers.CharField(source='employee.pk')
    terminal = serializers.CharField(source='terminal.pk', allow_null=True)
    zone = serializers.CharField(source='zone.pk')

    class Meta:
        model = Task
        fields = ('id', 'terminal', 'zone', 'type', 'status', 'result', 'employee', 'scanned_products')


class ZoneBackupSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='pk')
    tasks = TaskReadSerializer(many=True)

    prefetch_related_fields = ('tasks',)

    class Meta:
        model = Zone
        fields = (
            'id',
            'serial_number',
            'title',
            'storage_name',
            'code',
            'status',
            'is_auto_assignment',
            'tasks',
        )


class DocumentBackupSerializer(serializers.ModelSerializer):
    employee = serializers.CharField(source='employee.pk', allow_null=True)
    zone = serializers.CharField(source='zone.pk', allow_null=True)
    terminal = serializers.CharField(source='terminal.pk', allow_null=True)
    counter_scan_task = serializers.CharField(source='counter_scan_task.pk', allow_null=True)
    controller_task = serializers.CharField(source='controller_task.pk', allow_null=True)
    auditor_task = serializers.CharField(source='auditor_task.pk', allow_null=True)
    auditor_controller_task = serializers.CharField(source='auditor_controller_task.pk', allow_null=True)
    storage_task = serializers.CharField(source='storage_task.pk', allow_null=True)

    class Meta:
        model = Document
        fields = (
            'fake_id',
            'created_at',
            'employee',
            'status',
            'zone',
            'terminal',
            'counter_scan_task',
            'controller_task',
            'auditor_task',
            'auditor_controller_task',
            'storage_task',
            'start_audit_date',
            'end_audit_date',
            'tsd_number',
            'suspicious',
            'color',
            'color_changed',
        )


class EventBackupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('fake_id', 'created_at', 'title', 'comment')


class UserBackupSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='pk')

    class Meta:
        model = User
        fields = ('id', 'phone', 'username', 'first_name', 'middle_name', 'last_name')
