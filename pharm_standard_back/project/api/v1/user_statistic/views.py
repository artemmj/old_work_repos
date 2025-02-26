from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from api.v1.user_statistic.serializers import MonthStatsRequestSerializer
from api.v1.user_statistic.services import GetStatsService


class UserStatisticViewSet(GenericViewSet):

    @swagger_auto_schema(request_body=MonthStatsRequestSerializer, responses={200: None})
    @action(
        methods=['POST'],
        detail=False,
        url_path='month-by-username',
        url_name='user-statistics-month-by-username',
    )
    def months_by_username(self, request):
        serializer = MonthStatsRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ser = GetStatsService(serializer.data, request).process()
        return Response(ser)
