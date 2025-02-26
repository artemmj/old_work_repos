from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from api.v1.document.filters.filters import DocumentFilterSet
from api.v1.document.ordering import DocumentOrderingService
from api.v1.document.serializers import (  # noqa: WPS235
    AddProductPositionSerializer,
    BatchColorChangingRequestSerializer,
    BatchDiscrepancyReportRequestSerializer,
    BatchReplaceSpecificationRequestSerializer,
    BatchResetColorRequestSerializer,
    BatchStatusInvertingRequestSerializer,
    DeletePositionSerializer,
    DiscrepancyReportSerializer,
    DocumentBlockStatisticResponseSerializer,
    DocumentChangeColorSerializer,
    DocumentReadSerializer,
    DocumentReplaceSpecificationReadSerializer,
    DocumentWriteSerializer,
    InternalScannedProductSerializer,
    SetControllerSerializer,
)
from api.v1.document.services import (
    AddProductPositionService,
    BatchColorChangingService,
    BatchResetColorService,
    BatchStatusInvertingService,
    DeleteProductPositionService,
    SetDocumentControllerService,
)
from api.v1.document.services.batch_replace_documents_specification import BatchReplaceDocumentSpecificationService
from api.v1.document.services.get_documents import GetDocumentsService
from api.v1.document.services.replace_specification import ReplaceDocumentSpecificationService
from api.v1.document.services.statistic_block_service import DocumentStatisticBlockService
from api.v1.document.tasks import generate_batch_discrepancy_report_task, generate_discrepancy_report_task
from api.v1.product.serializers import ScannedProductSerializer
from apps.document.models import DocumentColorChoices
from apps.helpers.exceptions import ErrorResponseSerializer
from apps.helpers.serializers import EmptySerializer, EnumSerializer
from apps.helpers.viewsets import ListRetrieveCreateUpdateExtendedModelViewSet, paginate_response


class DocumentViewSet(ListRetrieveCreateUpdateExtendedModelViewSet):  # noqa: WPS214
    serializer_class = DocumentReadSerializer
    serializer_class_map = {
        'create': DocumentWriteSerializer,
        'update': DocumentWriteSerializer,
        'partial_update': DocumentWriteSerializer,
    }
    ordering_fields = (
        'id',
        'status',
        'zone__serial_number',
        'employee__roles',
        'counter_scan_barcode_amount',
        'controller_barcode_amount',
        'start_audit_date',
        'end_audit_date',
        'tsd_number',
        'employee__serial_number',
        'employee__username',
    )
    filterset_class = DocumentFilterSet
    filter_backends = (DjangoFilterBackend, OrderingFilter)

    def get_queryset(self):
        return GetDocumentsService().process()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        ordering_param = request.query_params.get('ordering')
        if ordering_param:
            queryset = DocumentOrderingService(queryset, ordering_param).process()

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(serializer.data)

    def partial_update(self, request, pk=None):
        document = self.get_object()
        serializer = self.get_serializer(document, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(document, serializer.validated_data)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=None,
        responses={
            200: DocumentBlockStatisticResponseSerializer,
            400: ErrorResponseSerializer,
        },
    )
    @action(methods=['get'], detail=False)
    def block_statistic(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        service = DocumentOrderingService(request, queryset)
        if hasattr(service, 'request'):
            queryset = service.process()
        serializer = DocumentReadSerializer(queryset, many=True, context={'request': request})
        result = DocumentStatisticBlockService(serializer_data=serializer.data).process()
        return Response(result)

    @swagger_auto_schema(responses={200: ScannedProductSerializer(many=True)})
    @action(['GET'], detail=True, url_path='scanned-products', url_name='scanned-products')
    def scanned_products(self, request, pk=None):
        document = self.get_object()
        scanned_products = []
        if document.counter_scan_task:
            scanned_products = [product for product in document.counter_scan_task.scanned_products.all()]  # noqa: C416
        serializer_data = ScannedProductSerializer(scanned_products, many=True).data

        # Необходимо динамически пронумеровать набор позиций
        for idx, scan_prd in enumerate(serializer_data, start=1):
            scan_prd['number'] = idx

        return paginate_response(self, serializer_data, InternalScannedProductSerializer, {'request': request})

    @swagger_auto_schema(request_body=DiscrepancyReportSerializer)
    @action(['POST'], detail=False, url_path='discrepancy-report', url_name='discrepancy-report')
    def discrepancy_report(self, request):
        serializer = DiscrepancyReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        endpoint_prefix = f'{request.scheme}://{request.META["HTTP_HOST"]}'
        task = generate_discrepancy_report_task.delay(serializer.data['document'], endpoint_prefix)
        return Response({'task_id': task.id})

    @swagger_auto_schema(request_body=DeletePositionSerializer, responses={200: DocumentReadSerializer})
    @action(['POST'], detail=True, url_path='delete-product-position', url_name='delete_product_position')
    def delete_product_position(self, request, pk=None):
        serializer = DeletePositionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service_result = DeleteProductPositionService(self.get_object(), serializer.data).process()
        return Response(DocumentReadSerializer(service_result).data)

    @swagger_auto_schema(request_body=AddProductPositionSerializer, responses={200: DocumentReadSerializer})
    @action(['POST'], detail=True, url_path='add-product-position', url_name='add-product-position')
    def add_product_position(self, request, pk=None):
        document = self.get_object()
        serializer = AddProductPositionSerializer(data=request.data, context={'project': document.zone.project})
        serializer.is_valid(raise_exception=True)
        service_result = AddProductPositionService(document, serializer.data).process()
        return Response(DocumentReadSerializer(service_result).data)

    @swagger_auto_schema(responses={200: EnumSerializer})
    @action(['GET'], detail=False, url_path='colors', url_name='document_colors')
    def colors(self, request):
        colors = DocumentColorChoices.choices
        return Response([{'value': color_value, 'name': color_name} for color_value, color_name in colors])

    @swagger_auto_schema(request_body=DocumentChangeColorSerializer, responses={200: DocumentReadSerializer})
    @action(['POST'], detail=True, url_path='change-color', url_name='document_change_color')
    def change_color(self, request, pk=None):
        serializer = DocumentChangeColorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        document = self.get_object()
        document.prev_color = document.color
        document.color = serializer.data['color']
        document.color_changed = True
        document.save()
        return Response(DocumentReadSerializer(document).data)

    @swagger_auto_schema(request_body=EmptySerializer, responses={200: DocumentReadSerializer})
    @action(['POST'], detail=True, url_path='reset-color', url_name='document_reset_color')
    def reset_color(self, request, pk=None):
        document = self.get_object()
        document.color = document.prev_color
        document.prev_color = None
        document.color_changed = False
        document.save()
        return Response(DocumentReadSerializer(document).data)

    @swagger_auto_schema(request_body=SetControllerSerializer, responses={200: DocumentReadSerializer})
    @action(['POST'], detail=True, url_path='set-controller', url_name='document_set_controller')
    def set_controller(self, request, pk=None):
        document = self.get_object()
        serializer = SetControllerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        document = SetDocumentControllerService(document=document, serializer_data=serializer.data).process()
        return Response(DocumentReadSerializer(document).data)

    @swagger_auto_schema(
        request_body=DocumentReplaceSpecificationReadSerializer,
        responses={200: DocumentReadSerializer},
    )
    @action(['POST'], detail=True, url_path='replace-specification', url_name='document_replace_specification')
    def replace_specification(self, request, pk=None):
        document = self.get_object()
        serializer = DocumentReplaceSpecificationReadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        document = ReplaceDocumentSpecificationService().process(validated_data['source'], document)
        return Response(DocumentReadSerializer(document).data)

    @swagger_auto_schema(
        request_body=BatchStatusInvertingRequestSerializer,
        responses={200: DocumentReadSerializer(many=True)},
    )
    @action(
        ['POST'],
        detail=False,
        url_path='batch-status-inverting',
        url_name='document_batch_status_inverting',
    )
    def batch_status_inverting(self, request):
        """Пакетное инвертирование статуса документа."""
        serializer = BatchStatusInvertingRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        documents = validated_data['document_ids']

        documents_ids = [document.id for document in documents]
        documents_with_virtual_attrs = GetDocumentsService().process().filter(id__in=documents_ids)

        documents_with_inverted_status = BatchStatusInvertingService(documents=documents_with_virtual_attrs).process()

        page = self.paginate_queryset(documents_with_inverted_status)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        request_body=BatchReplaceSpecificationRequestSerializer,
        responses={200: DocumentReadSerializer},
    )
    @action(
        ['POST'],
        detail=False,
        url_path='batch-specification-replacement',
        url_name='document_batch_specification_replacement',
    )
    def batch_specification_replacement(self, request):
        """Пакетная замена спецификации у документов."""
        serializer = BatchReplaceSpecificationRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        updated_documents = BatchReplaceDocumentSpecificationService(
            document_ids=validated_data['document_ids'],
            source=validated_data['source'],
        ).process()

        page = self.paginate_queryset(updated_documents)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        request_body=BatchColorChangingRequestSerializer,
        responses={200: DocumentReadSerializer},
    )
    @action(
        ['POST'],
        detail=False,
        url_path='batch-color-changing',
        url_name='document_batch_color_changing',
    )
    def batch_color_changing(self, request):
        """Пакетное изменение цвета документов."""
        serializer = BatchColorChangingRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        document_ids = validated_data['document_ids']
        color = validated_data['color']

        updated_documents = BatchColorChangingService(documents=document_ids, color=color).process()

        page = self.paginate_queryset(updated_documents)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        request_body=BatchResetColorRequestSerializer,
        responses={200: DocumentReadSerializer},
    )
    @action(
        ['POST'],
        detail=False,
        url_path='batch-reset-color',
        url_name='document_batch_reset_color',
    )
    def batch_reset_color(self, request):
        """Пакетное возвращение предыдущего цвета документов."""
        serializer = BatchResetColorRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        documents = validated_data['document_ids']

        updated_documents = BatchResetColorService(documents=documents).process()

        page = self.paginate_queryset(updated_documents)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @swagger_auto_schema(request_body=BatchDiscrepancyReportRequestSerializer)
    @action(
        ['POST'],
        detail=False,
        url_path='batch-discrepancy-report',
        url_name='document_batch_discrepancy_report',
    )
    def batch_discrepancy_report(self, request):
        """Пакетная генерация отчёта по расхождениям."""
        serializer = BatchDiscrepancyReportRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        endpoint_prefix = f'{request.scheme}://{request.META["HTTP_HOST"]}'

        task = generate_batch_discrepancy_report_task.delay(
            endpoint_prefix=endpoint_prefix,
            document_ids=serializer.validated_data['document_ids'],
        )
        return Response({'task_id': task.id})
