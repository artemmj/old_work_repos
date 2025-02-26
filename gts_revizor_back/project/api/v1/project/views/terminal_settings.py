from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.project.serializers.terminal_settings import (
    TerminalSettingsReadSerializer,
    TerminalSettingsUpdateSerializer,
)
from apps.helpers.exceptions import ErrorResponseSerializer
from apps.helpers.serializers import EnumSerializer
from apps.helpers.viewsets import RUExtendedModelViewSet
from apps.project.models import (
    CheckAMChoices,
    CheckDMChoices,
    IssuingTaskChoices,
    ProductNameChoices,
    RecalculationDiscrepancyChoices,
    TerminalSettings,
    UnknownBarcodeChoices,
)


class TerminalSettingsViewSet(RUExtendedModelViewSet):
    queryset = TerminalSettings.objects.all()
    serializer_class = TerminalSettingsUpdateSerializer
    serializer_class_map = {
        'retrieve': TerminalSettingsReadSerializer,
    }
    permission_classes = (permissions.AllowAny,)

    enum_responses = {
        200: EnumSerializer(many=True),
        404: ErrorResponseSerializer,
    }

    @swagger_auto_schema(responses=enum_responses)
    @action(methods=['get'], detail=False)
    def issuing_task_choices(self, request):
        return Response(EnumSerializer(IssuingTaskChoices, many=True).data)

    @swagger_auto_schema(responses=enum_responses)
    @action(methods=['get'], detail=False)
    def product_name_choices(self, request):
        return Response(EnumSerializer(ProductNameChoices, many=True).data)

    @swagger_auto_schema(responses=enum_responses)
    @action(methods=['get'], detail=False)
    def unknown_barcode_choices(self, request):
        return Response(EnumSerializer(UnknownBarcodeChoices, many=True).data)

    @swagger_auto_schema(responses=enum_responses)
    @action(methods=['get'], detail=False)
    def recalculation_discrepancy_choices(self, request):
        return Response(EnumSerializer(RecalculationDiscrepancyChoices, many=True).data)

    @swagger_auto_schema(responses=enum_responses)
    @action(methods=['get'], detail=False)
    def check_dm_choices(self, request):
        return Response(EnumSerializer(CheckDMChoices, many=True).data)

    @swagger_auto_schema(responses=enum_responses)
    @action(methods=['get'], detail=False)
    def check_am_choices(self, request):
        return Response(EnumSerializer(CheckAMChoices, many=True).data)
