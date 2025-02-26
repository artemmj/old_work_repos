from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.arketa.clients import ArketaTradepointApiClient
from apps.helpers.exceptions import ErrorResponseSerializer
from apps.user.permissions import IsApplicantConfirmedPermission, IsApplicantPermission, IsMasterPermission

from ..serializers import TradePointArketaVacantQuerySerializer, TradePointArketaVacantSerializer


class ArketaTradePointViewSet(ViewSet):
    permission_classes = (IsApplicantConfirmedPermission | IsApplicantPermission | IsMasterPermission,)

    @swagger_auto_schema(
        operation_summary='Список торговых точек с нераспределенными задачами.',
        query_serializer=TradePointArketaVacantQuerySerializer(),
        responses={
            status.HTTP_200_OK: TradePointArketaVacantSerializer(many=True),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        })
    @action(methods=['get'], detail=False)
    def vacant(self, request):
        serializer = TradePointArketaVacantQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        token = request.META.get('HTTP_AUTHORIZATION')
        service_result = ArketaTradepointApiClient(token).trade_point_vacant(serializer.data)
        return Response(service_result.get('results', {}))
