from rest_framework import serializers

from apps.employee.models import Employee
from apps.project.models import Project
from apps.task.models import TaskTypeChoices


class ReportCeleryResponseSerializer(serializers.Serializer):
    task_id = serializers.UUIDField()


class BaseProjectReportSerializer(serializers.Serializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    excel = serializers.BooleanField(required=True)


class InvThreeReportSerializer(BaseProjectReportSerializer):
    include = serializers.ChoiceField(
        choices=[
            ('all', 'Все'),
            ('only_identified', 'Только опознанные'),
            ('only_unidentified', 'Только неопознанные'),
            ('found_by_product_code', 'Найденные по коду товара'),
        ],
        required=True,
    )
    group_by = serializers.ChoiceField(
        choices=[
            ('by_barcode', 'По штрихкоду'),
            ('by_product_code', 'По коду товара'),
        ],
        required=True,
    )


class InvNinteenReportSerializer(InvThreeReportSerializer):
    pass  # noqa: WPS420 WPS604


class BarcodeMatchesReportSerializer(BaseProjectReportSerializer):
    include = serializers.ChoiceField(
        choices=[
            ('all', 'Все'),
            ('in_warehouses', 'В разрезе складов'),
        ],
        required=True,
    )
    less_than = serializers.IntegerField(help_text='Кол-во совпадений, не менее', required=True)


class DataMatrixMatchesReportSerializer(BaseProjectReportSerializer):
    group_by = serializers.ChoiceField(
        choices=[
            ('by_barcode', 'По штрихкоду'),
            ('by_product_code', 'По коду товара'),
        ],
        required=True,
    )


class CollationStatementTMCRReportSerializer(BaseProjectReportSerializer):
    group_by = serializers.ChoiceField(
        choices=[
            ('by_barcode', 'По штрихкоду'),
            ('by_product_code', 'По коду товара'),
        ],
        required=True,
    )
    discrepancy_in = serializers.ChoiceField(
        choices=[
            ('count', 'По количеству'),
            ('price', 'По цене'),
            ('sum', 'По сумме'),
        ],
        required=True,
    )
    more_than = serializers.IntegerField(required=True, min_value=0)


class NotFoundRestsReportSerializer(CollationStatementTMCRReportSerializer):
    discrepancy_in = serializers.ChoiceField(
        choices=[
            ('count', 'По количеству'),
            ('sum', 'По сумме'),
            ('price', 'По цене'),
        ],
    )


class InventoryInZonesReportSerializer(BaseProjectReportSerializer):
    serial_number_start = serializers.IntegerField(required=True)
    serial_number_end = serializers.IntegerField(required=True)


class DifferencesReportSerializer(BaseProjectReportSerializer):
    pass  # noqa: WPS420 WPS604


class NotCountedZonesReportSerializer(BaseProjectReportSerializer):
    pass  # noqa: WPS420 WPS604


class SuspiciousBarcodesReportSerializer(BaseProjectReportSerializer):
    pass  # noqa: WPS420 WPS604


class DiscAccountingQuantityReportSerializer(BaseProjectReportSerializer):
    group_by = serializers.ChoiceField(
        choices=[('by_barcode', 'По штрихкоду'), ('by_product_code', 'По коду товара')],
        required=True,
    )


class DiscrepanciesReportSerializer(BaseProjectReportSerializer):
    pass  # noqa: WPS420 WPS604


class ListOfDiscrepanciesReportSerializer(BaseProjectReportSerializer):
    only_discrepancies = serializers.BooleanField(required=True)


class AuditorReportSerializer(serializers.Serializer):
    excel = serializers.BooleanField(required=True)
    auditor = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
    task_type = serializers.ChoiceField(choices=[TaskTypeChoices.AUDITOR, TaskTypeChoices.AUDITOR_CONTROLLER])


class ErrorsReportSerializer(BaseProjectReportSerializer):
    pass  # noqa: WPS420 WPS604


class ProductsInZonesReportSerializer(BaseProjectReportSerializer):
    excel = serializers.BooleanField(required=False)
