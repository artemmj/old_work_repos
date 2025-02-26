from constance import admin, config
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.v1.settings.serializers import SelfInspectionPriceSettingSerializer, SettingsSerializer
from apps.helpers.permissions import IsAdministrator, IsDispatcher, IsSuperUser
from apps.helpers.viewsets import ExtendedViewSet


class SettingsViewSet(viewsets.ViewSet, ExtendedViewSet):
    serializer_class = SettingsSerializer
    permission_classes = (IsAuthenticated,)
    permission_map = {
        'self_inspection_price': (IsSuperUser | IsDispatcher | IsAdministrator),
        'change_self_inspection_price': (IsSuperUser | IsDispatcher | IsAdministrator),
    }

    @swagger_auto_schema(responses={200: SettingsSerializer(many=True)})
    def list(self, request):
        serializer = SettingsSerializer(admin.get_values().items(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def self_inspection_price(self, request):
        return Response(
            SettingsSerializer(('self_inspection_price', config.SELF_INSPECTION_PRICE)).data,
            status=status.HTTP_200_OK,
        )

    @action(methods=['get'], detail=False, permission_classes=(AllowAny,))
    def open(self, request):
        fields = ('policy', config.POLICY), ('user_agreenent', config.USER_AGREEMENT)
        return Response(SettingsSerializer(fields, many=True).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=SelfInspectionPriceSettingSerializer,
        responses={
            200: SettingsSerializer,
        },
    )
    @action(methods=['post'], detail=False)
    def change_self_inspection_price(self, request):
        """Изменить цену за самостоятельный осмотр."""
        serializer = SelfInspectionPriceSettingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        key = 'SELF_INSPECTION_PRICE'
        value = serializer.validated_data['value']  # noqa:  WPS110
        setattr(config, key, value)
        return Response(SettingsSerializer((key, value)).data, status=status.HTTP_200_OK)
