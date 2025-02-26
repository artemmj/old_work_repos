from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.response import Response

from api.v1.car.serializers.car import CarReadSerializer, CarWriteSerializer
from apps.car.models.car import Car
from apps.helpers.exceptions import BadRequestResponseSerializer
from apps.helpers.viewsets import ExtendedModelViewSet


class CarViewSet(ExtendedModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarReadSerializer
    serializer_class_map = {
        'create': CarWriteSerializer,
        'update': CarWriteSerializer,
        'partial_update': CarWriteSerializer,
    }

    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        request_body=CarWriteSerializer,
        responses={
            status.HTTP_201_CREATED: CarReadSerializer,
            status.HTTP_400_BAD_REQUEST: BadRequestResponseSerializer,
        },
    )
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            CarReadSerializer(instance=serializer.instance, context=self.get_serializer_context()).data,
            status=status.HTTP_201_CREATED,
        )

    @swagger_auto_schema(
        request_body=CarWriteSerializer,
        responses={
            status.HTTP_200_OK: CarReadSerializer,
            status.HTTP_400_BAD_REQUEST: BadRequestResponseSerializer,
        },
    )
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}  # noqa: WPS437
        return Response(
            CarReadSerializer(instance=serializer.instance, context=self.get_serializer_context()).data,
            status=status.HTTP_200_OK,
        )
