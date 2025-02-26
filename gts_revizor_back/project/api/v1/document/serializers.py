from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.v1.employee.serializers import EmployeeShortReadSerializer
from api.v1.product.serializers import ProductReadSerializer
from api.v1.zone.serializers import ZoneReadCompactSerializer
from apps.document.models import Document, DocumentColorChoices, DocumentStatusChoices
from apps.employee.models import EmployeeRoleChoices
from apps.event.models import Event, TitleChoices
from apps.helpers.serializers import EagerLoadingSerializerMixin, EnumField
from apps.product.models import Product, ScannedProduct
from apps.task.models import Task, TaskStatusChoices, TaskTypeChoices
from apps.zone.models import ZoneStatusChoices


class ChooseControllersSerializer(serializers.Serializer):
    username = serializers.CharField()
    task = serializers.UUIDField()
    result = serializers.IntegerField()


class DocumentReadSerializer(serializers.ModelSerializer, EagerLoadingSerializerMixin):  # noqa: WPS214
    status = EnumField(enum_class=DocumentStatusChoices)
    zone = ZoneReadCompactSerializer()
    employee = EmployeeShortReadSerializer()

    counter_scan = serializers.SerializerMethodField(help_text='Счетчик', read_only=True)
    controller = serializers.SerializerMethodField(help_text='УК', read_only=True)
    auditor = serializers.SerializerMethodField(help_text='Аудитор', read_only=True)
    auditor_discrepancy = serializers.SerializerMethodField(read_only=True)
    auditor_controller = serializers.SerializerMethodField(help_text='Аудитор УК', read_only=True)
    auditor_controller_discrepancy = serializers.SerializerMethodField(read_only=True)
    auditor_external = serializers.SerializerMethodField(help_text='Внешний аудитор', read_only=True)
    auditor_external_discrepancy = serializers.SerializerMethodField(read_only=True)
    storage = serializers.SerializerMethodField(help_text='Сотрудник склада', read_only=True)
    choose_controllers = serializers.SerializerMethodField(read_only=True)

    prefetch_related_fields = ('zone__tasks',)

    class Meta:
        model = Document
        fields = (
            'id',
            'fake_id',
            'created_at',
            'status',
            'zone',
            'employee',
            'counter_scan',
            'controller',
            'auditor',
            'auditor_discrepancy',
            'auditor_controller',
            'auditor_controller_discrepancy',
            'auditor_external',
            'auditor_external_discrepancy',
            'storage',
            'start_audit_date',
            'end_audit_date',
            'tsd_number',
            'suspicious',
            'color',
            'color_changed',
            'choose_controllers',
            'is_replace_specification',
        )

    def get_counter_scan(self, instance) -> int:
        return instance.counter_scan_task.result if instance.counter_scan_task else None

    def get_controller(self, instance) -> int:
        if instance.controller_task:
            return instance.controller_task.result
        return None

    def get_auditor(self, instance) -> int:
        return instance.auditor_task.result if instance.auditor_task else None

    def get_auditor_discrepancy(self, instance) -> bool:
        # аудитор проверяет счетчик по шк
        from api.v1.document.services import CheckAuditorDiscrepancyService  # noqa: WPS433
        if instance.counter_scan_task and instance.auditor_task:
            return CheckAuditorDiscrepancyService().process(instance.counter_scan_task, instance.auditor_task)
        return False

    def get_auditor_controller(self, instance) -> int:
        if instance.auditor_controller_task and instance.auditor_controller_task:  # noqa: WPS408
            return instance.auditor_controller_task.result
        return None

    def get_auditor_controller_discrepancy(self, instance) -> bool:
        # аудитор ук проверят ук просто цифру
        if instance.controller_task and instance.auditor_controller_task:
            return instance.controller_task.result != instance.auditor_controller_task.result
        return False

    def get_auditor_external(self, instance) -> bool:
        if instance.auditor_external_task and instance.auditor_external_task.result:
            return instance.auditor_external_task.result
        return None

    def get_auditor_external_discrepancy(self, instance) -> bool:
        # внеш. аудитор проверят счетчик по шк
        from api.v1.document.services import CheckAuditorDiscrepancyService  # noqa: WPS433
        if instance.counter_scan_task and instance.auditor_external_task:
            return CheckAuditorDiscrepancyService().process(instance.counter_scan_task, instance.auditor_external_task)
        return False

    def get_storage(self, instance) -> int:
        return instance.storage_task.result if instance.storage_task and instance.storage_task.result else None

    @swagger_serializer_method(serializer_or_field=ChooseControllersSerializer(many=True))
    def get_choose_controllers(self, obj) -> dict:
        choose_controllers = []
        statuss = (
            TaskStatusChoices.WORKED,
            TaskStatusChoices.SUCCESS_SCAN,
            TaskStatusChoices.FAILED_SCAN,
        )
        for task in obj.zone.tasks.filter(type=TaskTypeChoices.CONTROLLER, status__in=statuss):
            choose_controllers.append({
                'username': task.employee.username if (hasattr(task, 'employee') and task.employee) else None,
                'task': task.pk,
                'result': task.result,
            })
        return choose_controllers


class DocumentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = (
            'id',
            'created_at',
            'status',
            'zone',
            'employee',
            'start_audit_date',
            'end_audit_date',
            'tsd_number',
        )
        read_only_fields = ('id', 'created_at')

    def update(self, instance, validated_data):  # noqa: WPS231
        if 'status' in validated_data:
            # При ручной установке какого-то документа в статус готово его в зеленый цвет, остальные в зоне белый
            for doc in Document.objects.filter(zone=instance.zone).exclude(pk=instance.pk):
                doc.color = DocumentColorChoices.WHITE
                doc.status = DocumentStatusChoices.NOT_READY
                doc.save()

            if validated_data['status'] == DocumentStatusChoices.READY:  # noqa: WPS529
                validated_data['color'] = DocumentColorChoices.GREEN
                instance.zone.status = ZoneStatusChoices.READY
                # При ручной установке в Готово считаем что таски сошлась
                instance.counter_scan_task.status = TaskStatusChoices.SUCCESS_SCAN
                if getattr(instance, 'controller_task', False):
                    instance.controller_task.status = TaskStatusChoices.SUCCESS_SCAN
            elif validated_data['status'] == DocumentStatusChoices.NOT_READY:  # noqa: WPS529
                validated_data['color'] = DocumentColorChoices.RED
                instance.zone.status = ZoneStatusChoices.NOT_READY
                # При ручной установке в Не готово считаем что таски не сошлась
                instance.counter_scan_task.status = TaskStatusChoices.FAILED_SCAN
                if getattr(instance, 'controller_task', False):
                    instance.controller_task.status = TaskStatusChoices.FAILED_SCAN
            instance.counter_scan_task.save(update_fields=['status'])

        instance = super().update(instance, validated_data)
        instance.zone.save(update_fields=['status'])

        Event.objects.create(
            project=instance.zone.project,
            title=TitleChoices.DOCUMENT_CHANGE_STATUS,
            comment=(
                f'Изменен статус документа; зона: {instance.zone}, документ: {instance.pk}, '
                f'новый статус: "{instance.get_status_display()}"'  # noqa: WPS326
            ),
        )
        return instance


class DiscrepancyReportSerializer(serializers.Serializer):
    document = serializers.PrimaryKeyRelatedField(queryset=Document.objects.all())


class DeletePositionSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=ScannedProduct.objects.all(), required=True)


class AddProductPositionSerializer(serializers.Serializer):
    barcode = serializers.CharField(required=True)
    amount = serializers.IntegerField(required=True)

    def validate_barcode(self, barcode: str):
        try:
            Product.objects.get(barcode=barcode, project=self.context['project'])
        except Product.DoesNotExist:
            raise ValidationError('Не найден товар с таким barcode.')
        return barcode


class InternalScannedProductSerializer(serializers.ModelSerializer):

    class ProductReadSerializer(EagerLoadingSerializerMixin, serializers.ModelSerializer):  # noqa: WPS431
        title = serializers.SerializerMethodField()

        class Meta:
            model = Product
            fields = ('id', 'vendor_code', 'barcode', 'title', 'remainder', 'price', 'am', 'dm', 'size')
            read_only_fields = ('id',)

        def get_title(self, instance):
            if instance.get('size'):
                return f'{instance.get("title")}, {instance.get("size")}'
            return instance.get('title')

    number = serializers.IntegerField()
    product = ProductReadSerializer()

    class Meta:
        model = ScannedProduct
        fields = ('id', 'created_at', 'scanned_time', 'number', 'product', 'amount', 'dm')


class DocumentChangeColorSerializer(serializers.Serializer):
    color = serializers.ChoiceField(choices=DocumentColorChoices.choices)


class SetControllerSerializer(serializers.Serializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(), required=True)


class DocumentBlockStatisticResponseSerializer(serializers.Serializer):
    docs_count = serializers.IntegerField()
    count_sum = serializers.FloatField()
    count_aver = serializers.FloatField()


class DocumentReplaceSpecificationReadSerializer(serializers.Serializer):
    source = serializers.ChoiceField(choices=[EmployeeRoleChoices.AUDITOR, EmployeeRoleChoices.AUDITOR_EXTERNAL])


class BatchStatusInvertingRequestSerializer(serializers.Serializer):
    document_ids = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=Document.objects.all()),
        required=True,
    )


class BatchReplaceSpecificationRequestSerializer(serializers.Serializer):
    document_ids = serializers.ListField(child=serializers.IntegerField(min_value=0))
    source = serializers.ChoiceField(choices=[EmployeeRoleChoices.AUDITOR, EmployeeRoleChoices.AUDITOR_EXTERNAL])


class BatchColorChangingRequestSerializer(serializers.Serializer):
    document_ids = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=Document.objects.all()),
        required=True,
    )
    color = serializers.ChoiceField(choices=DocumentColorChoices.choices)


class BatchResetColorRequestSerializer(serializers.Serializer):
    document_ids = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=Document.objects.all()),
        required=True,
    )


class BatchDiscrepancyReportRequestSerializer(serializers.Serializer):
    document_ids = serializers.ListField(child=serializers.IntegerField(min_value=0))


class DocumentScannedProductsReadSerializer(serializers.ModelSerializer):
    product = ProductReadSerializer()
    number = serializers.IntegerField()
    displayed_dm = serializers.CharField()

    class Meta:
        model = ScannedProduct
        fields = (
            'id',
            'created_at',
            'scanned_time',
            'number',
            'product',
            'amount',
            'added_by_product_code',
            'dm',
            'displayed_dm',
        )
