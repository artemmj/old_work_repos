from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.car.filters.modification import ModificationFilterSet
from api.v1.car.serializers.modification import CarTypeEnumSerializer, ModificationReadSerializer
from apps.car.models import BodyTypeChoices, DriveTypeChoices, EngineTypeChoices, GearboxTypeChoices
from apps.car.models.modification import Modification
from apps.helpers.viewsets import ExtendedViewSet


class ModificationViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, ExtendedViewSet):  # noqa: WPS338
    queryset = Modification.objects.all()
    serializer_class = ModificationReadSerializer
    serializer_class_map = {
        'list': ModificationReadSerializer,
        'retrieve': ModificationReadSerializer,
    }

    filterset_class = ModificationFilterSet
    permission_classes = (permissions.IsAuthenticated,)

    def _response_types(self, enum_class, type_field):
        types = [{'value': i[0], 'name': i[1]} for i in enum_class.choices]   # noqa: WPS221, WPS338
        if self.request.query_params:
            qs = self.filter_queryset(self.queryset).values_list(type_field, flat=True).distinct()
            types = list(filter(lambda x: x['value'] in qs, types))
        return Response(CarTypeEnumSerializer(types, many=True).data)

    @swagger_auto_schema(responses={200: CarTypeEnumSerializer(many=True)})
    @action(methods=['get'], detail=False)
    def body_type_choices(self, request):
        """Возвращает возможные типы кузова."""
        return self._response_types(BodyTypeChoices, 'body_type')

    @swagger_auto_schema(responses={200: CarTypeEnumSerializer(many=True)})
    @action(methods=['get'], detail=False)
    def gearbox_type_choices(self, request):
        """Возвращает возможные типы коробок."""
        return self._response_types(GearboxTypeChoices, 'gearbox_type')

    @swagger_auto_schema(responses={200: CarTypeEnumSerializer(many=True)})
    @action(methods=['get'], detail=False)
    def engine_type_choices(self, request):
        """Возвращает возможные типы двигателей."""
        return self._response_types(EngineTypeChoices, 'engine_type')

    @swagger_auto_schema(responses={200: CarTypeEnumSerializer(many=True)})
    @action(methods=['get'], detail=False)
    def drive_type_choices(self, request):
        """Возвращает возможные типы привода."""
        return self._response_types(DriveTypeChoices, 'drive_type')
