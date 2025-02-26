from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.address.serializers import (
    AddressDadataQuerySerializer,
    AddressDadataResultSerializer,
    AddressReadSerializer,
    AddressWriteSerializer,
)
from apps.address.models import Address
from apps.dadata.services import DadataSearchAddressService
from apps.helpers.viewsets import ExtendedModelViewSet


class AddressViewSet(ExtendedModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressReadSerializer
    serializer_class_map = {
        'create': AddressWriteSerializer,
        'update': AddressWriteSerializer,
        'partial_update': AddressWriteSerializer,
    }

    @swagger_auto_schema(
        request_body=AddressWriteSerializer,
        responses={
            status.HTTP_201_CREATED: AddressReadSerializer(many=True),
        },
    )
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(AddressReadSerializer(instance).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}  # noqa: WPS437

        return Response(AddressReadSerializer(instance=instance).data)

    @swagger_auto_schema(
        query_serializer=AddressDadataQuerySerializer,
        responses={
            status.HTTP_200_OK: AddressDadataResultSerializer(many=True),
        },
    )
    @action(methods=['get'], detail=False, url_path='dadata/search_address')
    def dadata_search_address(self, request):  # noqa: WPS210
        """Вернет найденные варианты адресов."""
        query_serializer = AddressDadataQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        query = query_serializer.validated_data.get('query')
        lat = query_serializer.validated_data.get('lat')
        lon = query_serializer.validated_data.get('lon')
        result = DadataSearchAddressService().process(query=query, lat=lat, lon=lon)  # noqa: WPS110
        serializer = AddressDadataResultSerializer(result, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
