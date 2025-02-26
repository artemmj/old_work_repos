from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from api.v1.reports import serializers
from api.v1.reports.services import (  # noqa: WPS235
    generate_auditor_report_task,
    generate_barcode_matches_report_task,
    generate_collation_statement_report_task,
    generate_differences_report_task,
    generate_disc_accounting_quantity_report_task,
    generate_discrepancies_report_task,
    generate_errors_report_task,
    generate_inv_in_zones_report_task,
    generate_inv_ninteen_report_task,
    generate_inv_three_report_task,
    generate_list_of_discrepancies_report_task,
    generate_not_counted_zones_report_task,
    generate_not_found_rests_report_task,
    generate_products_in_zones_report,
    generate_suspicious_barcodes_report_task,
)


class ReportsViewSet(ViewSet):  # noqa: WPS214

    @swagger_auto_schema(
        method='POST',
        request_body=serializers.InvThreeReportSerializer,
        responses={200: serializers.ReportCeleryResponseSerializer},
    )
    @action(['POST'], detail=False, url_name='inv-3', url_path='inv-3')
    def inv_three(self, request, *args, **kwargs):
        """Отчет ИНВ-3."""
        serializer = serializers.InvThreeReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # noqa: WPS204
        endpoint_prefix = f'{request.scheme}://{request.META["HTTP_HOST"]}'  # noqa: WPS204
        task = generate_inv_three_report_task.delay(serializer.data, endpoint_prefix)
        return Response({'task_id': task.id})  # noqa: WPS204

    @swagger_auto_schema(
        method='POST',
        request_body=serializers.InvNinteenReportSerializer,
        responses={200: serializers.ReportCeleryResponseSerializer},
    )
    @action(['POST'], detail=False, url_name='inv-19', url_path='inv-19')
    def inv_ninteen(self, request, *args, **kwargs):
        """Отчет ИНВ-19."""
        serializer = serializers.InvNinteenReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        endpoint_prefix = f'{request.scheme}://{request.META["HTTP_HOST"]}'
        task = generate_inv_ninteen_report_task.delay(serializer.data, endpoint_prefix)
        return Response({'task_id': task.id})

    @swagger_auto_schema(
        method='POST',
        request_body=serializers.BarcodeMatchesReportSerializer,
        responses={200: serializers.ReportCeleryResponseSerializer},
    )
    @action(['POST'], detail=False, url_name='barcode-matches', url_path='barcode-matches')
    def barcode_matches(self, request, *args, **kwargs):
        """Совпадение ШК по зонам."""
        serializer = serializers.BarcodeMatchesReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        endpoint_prefix = f'{request.scheme}://{request.META["HTTP_HOST"]}'
        task = generate_barcode_matches_report_task.delay(serializer.data, endpoint_prefix, by_barcode=True)
        return Response({'task_id': task.id})

    @swagger_auto_schema(
        method='POST',
        request_body=serializers.DataMatrixMatchesReportSerializer,
        responses={200: serializers.ReportCeleryResponseSerializer},
    )
    @action(['POST'], detail=False, url_name='data-matrix-matches', url_path='data-matrix-matches')
    def data_matrix_matches(self, request, *args, **kwargs):
        """Совпадение DM по зонам."""
        serializer = serializers.DataMatrixMatchesReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        endpoint_prefix = f'{request.scheme}://{request.META["HTTP_HOST"]}'
        task = generate_barcode_matches_report_task.delay(serializer.data, endpoint_prefix, by_barcode=False)
        return Response({'task_id': task.id})

    @swagger_auto_schema(
        method='POST',
        request_body=serializers.CollationStatementTMCRReportSerializer,
        responses={200: serializers.ReportCeleryResponseSerializer},
    )
    @action(['POST'], detail=False, url_name='diff-zones', url_path='diff-zones')
    def collation_statement_tmc(self, request, *args, **kwargs):
        """Отчет Расхождения по зонам (Счислительная ведомость ТМЦ по зонам)."""
        serializer = serializers.CollationStatementTMCRReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        endpoint_prefix = f'{request.scheme}://{request.META["HTTP_HOST"]}'
        task = generate_collation_statement_report_task.delay(serializer.data, endpoint_prefix)
        return Response({'task_id': task.id})

    @swagger_auto_schema(
        method='POST',
        request_body=serializers.NotFoundRestsReportSerializer,
        responses={200: serializers.ReportCeleryResponseSerializer},
    )
    @action(['POST'], detail=False, url_name='not-found-rests', url_path='not-found-rests')
    def not_found_rests(self, request, *args, **kwargs):
        """Ненайденные остатки."""
        serializer = serializers.NotFoundRestsReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        endpoint_prefix = f'{request.scheme}://{request.META["HTTP_HOST"]}'
        task = generate_not_found_rests_report_task.delay(serializer.data, endpoint_prefix)
        return Response({'task_id': task.id})

    @swagger_auto_schema(
        method='POST',
        request_body=serializers.AuditorReportSerializer,
        responses={200: serializers.ReportCeleryResponseSerializer},
    )
    @action(['POST'], detail=False, url_name='auditor-report', url_path='auditor-report')
    def auditor_report(self, request, *args, **kwargs):
        """Отчет аудитора."""
        serializer = serializers.AuditorReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        endpoint_prefix = f'{request.scheme}://{request.META["HTTP_HOST"]}'
        task = generate_auditor_report_task.delay(serializer.data, endpoint_prefix)
        return Response({'task_id': task.id})

    @swagger_auto_schema(
        method='POST',
        request_body=serializers.InventoryInZonesReportSerializer,
        responses={200: serializers.ReportCeleryResponseSerializer},
    )
    @action(['POST'], detail=False, url_name='inv-in-zones', url_path='inv-in-zones')
    def inventory_in_zones(self, request, *args, **kwargs):
        """Общее кол-во ТМЦ по зонам."""
        serializer = serializers.InventoryInZonesReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        endpoint_prefix = f'{request.scheme}://{request.META["HTTP_HOST"]}'
        task = generate_inv_in_zones_report_task.delay(serializer.data, endpoint_prefix)
        return Response({'task_id': task.id})

    @swagger_auto_schema(
        method='POST',
        request_body=serializers.DifferencesReportSerializer,
        responses={200: serializers.ReportCeleryResponseSerializer},
    )
    @action(['POST'], detail=False, url_name='differences', url_path='differences')
    def differences(self, request, *args, **kwargs):
        """Ре Трейдинг счислительная (Отчет по расхождениям)."""
        serializer = serializers.DifferencesReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        endpoint_prefix = f'{request.scheme}://{request.META["HTTP_HOST"]}'
        task = generate_differences_report_task.delay(serializer.data, endpoint_prefix)
        return Response({'task_id': task.id})

    @swagger_auto_schema(
        method='POST',
        request_body=serializers.NotCountedZonesReportSerializer,
        responses={200: serializers.ReportCeleryResponseSerializer},
    )
    @action(['POST'], detail=False, url_name='not-counted-zones', url_path='not-counted-zones')
    def not_counted_zones(self, request, *args, **kwargs):
        """Непросчитанные зоны."""
        serializer = serializers.NotCountedZonesReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        endpoint_prefix = f'{request.scheme}://{request.META["HTTP_HOST"]}'
        task = generate_not_counted_zones_report_task.delay(serializer.data, endpoint_prefix)
        return Response({'task_id': task.id})

    @swagger_auto_schema(
        method='POST',
        request_body=serializers.SuspiciousBarcodesReportSerializer,
        responses={200: serializers.ReportCeleryResponseSerializer},
    )
    @action(['POST'], detail=False, url_name='suspicious-barcodes', url_path='suspicious-barcodes')
    def suspicious_barcodes(self, request, *args, **kwargs):
        """Отчет по подозрительным ШК."""
        serializer = serializers.SuspiciousBarcodesReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        endpoint_prefix = f'{request.scheme}://{request.META["HTTP_HOST"]}'
        task = generate_suspicious_barcodes_report_task.delay(serializer.data, endpoint_prefix)
        return Response({'task_id': task.id})

    @swagger_auto_schema(
        method='POST',
        request_body=serializers.DiscAccountingQuantityReportSerializer,
        responses={200: serializers.ReportCeleryResponseSerializer},
    )
    @action(['POST'], detail=False, url_name='disc-accounting-quantity', url_path='disc-accounting-quantity')
    def disc_accounting_quantity(self, request, *args, **kwargs):
        """Расхождения с учетным кол-вом."""
        serializer = serializers.DiscAccountingQuantityReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        endpoint_prefix = f'{request.scheme}://{request.META["HTTP_HOST"]}'
        task = generate_disc_accounting_quantity_report_task.delay(serializer.data, endpoint_prefix)
        return Response({'task_id': task.id})

    @swagger_auto_schema(
        method='POST',
        request_body=serializers.DiscrepanciesReportSerializer,
        responses={200: serializers.ReportCeleryResponseSerializer},
    )
    @action(['POST'], detail=False, url_name='lg-numeral', url_path='lg-numeral')
    def lg_numeral(self, request, *args, **kwargs):
        """L&G сличительная (Ведомость расхождений)."""
        serializer = serializers.DiscrepanciesReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        endpoint_prefix = f'{request.scheme}://{request.META["HTTP_HOST"]}'
        task = generate_discrepancies_report_task.delay(serializer.data, endpoint_prefix)
        return Response({'task_id': task.id})

    @swagger_auto_schema(
        method='POST',
        request_body=serializers.ListOfDiscrepanciesReportSerializer,
        responses={200: serializers.ReportCeleryResponseSerializer},
    )
    @action(['POST'], detail=False, url_name='list-of-discrepancies', url_path='list-of-discrepancies')
    def list_of_discrepancies(self, request, *args, **kwargs):
        """Ведомость расхождения."""
        serializer = serializers.ListOfDiscrepanciesReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        endpoint_prefix = f'{request.scheme}://{request.META["HTTP_HOST"]}'
        task = generate_list_of_discrepancies_report_task.delay(serializer.data, endpoint_prefix)
        return Response({'task_id': task.id})

    @swagger_auto_schema(
        method='POST',
        request_body=serializers.ProductsInZonesReportSerializer,
        responses={200: serializers.ReportCeleryResponseSerializer},
    )
    @action(['POST'], detail=False, url_name='products-in-zones', url_path='products-in-zones')
    def products_in_zones(self, request, *args, **kwargs):
        """Товары в зонах."""
        serializer = serializers.ProductsInZonesReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        endpoint_prefix = f'{request.scheme}://{request.META["HTTP_HOST"]}'
        task = generate_products_in_zones_report.delay(serializer.data, endpoint_prefix)
        return Response({'task_id': task.id})

    @swagger_auto_schema(
        method='POST',
        request_body=serializers.ErrorsReportSerializer,
        responses={200: serializers.ReportCeleryResponseSerializer},
    )
    @action(['POST'], detail=False, url_name='errors-reports', url_path='errors-report')
    def errors_report(self, request, *args, **kwargs):
        """Отчет по ошибкам."""
        serializer = serializers.ErrorsReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        endpoint_prefix = f'{request.scheme}://{request.META["HTTP_HOST"]}'
        task = generate_errors_report_task.delay(serializer.data, endpoint_prefix)
        return Response({'task_id': task.id})
