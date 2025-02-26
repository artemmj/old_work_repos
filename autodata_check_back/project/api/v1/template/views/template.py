from constance import config
from django.db.models import Q  # noqa: WPS347
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response

from api.v1.template.filters import TemplateFilterSet
from api.v1.template.serializers import (  # noqa: WPS235
    TemplateClientSerializer,
    TemplateCompletenessSerializer,
    TemplateDamageSerializer,
    TemplateDocumentsSerializer,
    TemplateEquipmentSerializer,
    TemplateLiftSerializer,
    TemplatePaintworkSerializer,
    TemplatePhotosSerializer,
    TemplatePlaceSerializer,
    TemplateReadSerializer,
    TemplateSerializer,
    TemplateSignaturesSerializer,
    TemplateTechnicalSerializer,
    TemplateTiresSerializer,
    TemplateVideoSerializer,
)
from api.v1.template.serializers.template import TemplateCompactSerializer, TemplateUpdateSerializer
from apps.helpers.exceptions import BadRequestResponseSerializer
from apps.helpers.permissions import IsAdministrator, IsDispatcher
from apps.helpers.viewsets import ExtendedModelViewSet, paginate_response
from apps.template.models import Template


class TemplateViewSet(ExtendedModelViewSet):  # noqa: WPS338, WPS214
    queryset = Template.objects.all()
    serializer_class = TemplateReadSerializer
    serializer_class_map = {
        'compact': TemplateCompactSerializer,
        'create': TemplateSerializer,
        'partial_update': TemplateUpdateSerializer,
        'active': TemplateReadSerializer,
        'update_equipment': TemplateEquipmentSerializer,
        'update_completeness': TemplateCompletenessSerializer,
        'update_documents': TemplateDocumentsSerializer,
        'update_tires': TemplateTiresSerializer,
        'update_photos': TemplatePhotosSerializer,
        'update_paintwork': TemplatePaintworkSerializer,
        'update_damage': TemplateDamageSerializer,
        'update_technical': TemplateTechnicalSerializer,
        'update_lift': TemplateLiftSerializer,
        'update_video': TemplateVideoSerializer,
        'update_place': TemplatePlaceSerializer,
        'update_client': TemplateClientSerializer,
        'update_signatures': TemplateSignaturesSerializer,
    }
    permission_classes = (permissions.IsAuthenticated,)
    permission_map = {
        'compact': (IsAdministrator | IsDispatcher),
    }
    http_method_names = ('get', 'post', 'patch', 'delete')
    filterset_class = TemplateFilterSet
    ordering_fields = (
        'title',
        'user__last_name',
        'user__phone',
        'is_main',
        'is_accreditation',
        'created_at',
    )

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-is_main', '-is_active')
        if (IsAdministrator | IsDispatcher)().has_permission(self.request, self):
            return queryset
        return queryset.filter(Q(user=self.request.user) | Q(is_main=True) | Q(is_accreditation=True))  # noqa: WPS221

    @action(methods=['get'], detail=False, url_path='compact')
    def compact(self, request):
        """Компактный список шаблонов."""
        queryset = self.filter_queryset(self.get_queryset())
        return paginate_response(self, queryset=queryset)

    responses = {
        status.HTTP_200_OK: TemplateReadSerializer(),
        status.HTTP_400_BAD_REQUEST: BadRequestResponseSerializer(),
    }

    @swagger_auto_schema(request_body=TemplateUpdateSerializer, responses=responses)
    def partial_update(self, request, *args, **kwargs):
        """Обновить шаблон."""
        instance = self.get_object()  # noqa: DAR401

        is_adm_disp = (IsAdministrator | IsDispatcher)().has_permission(self.request, self)
        if not is_adm_disp and instance.is_active and (instance.is_main or instance.is_accreditation):
            raise PermissionDenied()

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}  # noqa: WPS437
        return Response(TemplateReadSerializer(instance=instance).data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """Удалить шаблон."""  # noqa: DAR401c
        instance = self.get_object()
        is_active = instance.is_active
        if self.queryset.count() == 1:
            raise ValidationError({'error': config.TEMPLATE_DESTROY_LAST_TEMPLATE_ERROR})
        self.perform_destroy(instance)
        if is_active:
            instance = self.queryset.first()
            instance.is_active = True
            instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(responses={
        status.HTTP_200_OK: TemplateReadSerializer,
        status.HTTP_400_BAD_REQUEST: BadRequestResponseSerializer,
    })
    @action(methods=['get'], detail=False)
    def active(self, request):
        """Получить активный шаблон."""
        instance = get_object_or_404(
            Template, user=request.user, is_active=True, is_main=False, is_accreditation=False,
        )
        serializer = self.get_serializer(instance=instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def _update_settings(self, request, instance, setting_obj):
        serializer = self.get_serializer(setting_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(TemplateReadSerializer(instance=instance).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=TemplateEquipmentSerializer, responses=responses)
    @action(methods=['patch'], detail=True)
    def update_equipment(self, request, pk=None):
        """Обновить настройки комплектации."""
        instance = self.get_object()
        equipment = instance.equipment
        return self._update_settings(request, instance, equipment)

    @swagger_auto_schema(request_body=TemplateCompletenessSerializer, responses=responses)
    @action(methods=['patch'], detail=True)
    def update_completeness(self, request, pk=None):
        """Обновить настройки комплектности."""
        instance = self.get_object()
        completeness = instance.completeness
        return self._update_settings(request, instance, completeness)

    @swagger_auto_schema(request_body=TemplateDocumentsSerializer, responses=responses)
    @action(methods=['patch'], detail=True)
    def update_documents(self, request, pk=None):
        """Обновить настройки документов."""
        instance = self.get_object()
        documents = instance.documents
        return self._update_settings(request, instance, documents)

    @swagger_auto_schema(request_body=TemplateTiresSerializer, responses=responses)
    @action(methods=['patch'], detail=True)
    def update_tires(self, request, pk=None):
        """Обновить настройки шин."""
        instance = self.get_object()
        tires = instance.tires
        return self._update_settings(request, instance, tires)

    @swagger_auto_schema(request_body=TemplatePhotosSerializer, responses=responses)
    @action(methods=['patch'], detail=True)
    def update_photos(self, request, pk=None):
        """Обновить настройки фотографий."""
        instance = self.get_object()
        photos = instance.photos
        return self._update_settings(request, instance, photos)

    @swagger_auto_schema(request_body=TemplatePaintworkSerializer, responses=responses)
    @action(methods=['patch'], detail=True)
    def update_paintwork(self, request, pk=None):
        """Обновить настройки ЛКП."""
        instance = self.get_object()
        paintwork = instance.paintwork
        return self._update_settings(request, instance, paintwork)

    @swagger_auto_schema(request_body=TemplateDamageSerializer, responses=responses)
    @action(methods=['patch'], detail=True)
    def update_damage(self, request, pk=None):
        """Обновить настройки повреждений."""
        instance = self.get_object()
        damage = instance.damage
        return self._update_settings(request, instance, damage)

    @swagger_auto_schema(request_body=TemplateTechnicalSerializer, responses=responses)
    @action(methods=['patch'], detail=True)
    def update_technical(self, request, pk=None):
        """Обновить настройки технического состояния."""
        instance = self.get_object()
        technical = instance.technical
        return self._update_settings(request, instance, technical)

    @swagger_auto_schema(request_body=TemplateLiftSerializer, responses=responses)
    @action(methods=['patch'], detail=True)
    def update_lift(self, request, pk=None):
        """Обновить настройки осмотра на подъемнике."""
        instance = self.get_object()
        lift = instance.lift
        return self._update_settings(request, instance, lift)

    @swagger_auto_schema(request_body=TemplateVideoSerializer, responses=responses)
    @action(methods=['patch'], detail=True)
    def update_video(self, request, pk=None):
        """Обновить настройки видео."""
        instance = self.get_object()
        video = instance.video
        return self._update_settings(request, instance, video)

    @swagger_auto_schema(request_body=TemplatePlaceSerializer, responses=responses)
    @action(methods=['patch'], detail=True)
    def update_place(self, request, pk=None):
        """Обновить настройки места осмотра."""
        instance = self.get_object()
        place = instance.place
        return self._update_settings(request, instance, place)

    @swagger_auto_schema(request_body=TemplateClientSerializer, responses=responses)
    @action(methods=['patch'], detail=True)
    def update_client(self, request, pk=None):
        """Обновить настройки данных клиента."""
        instance = self.get_object()
        client = instance.client
        return self._update_settings(request, instance, client)

    @swagger_auto_schema(request_body=TemplateSignaturesSerializer, responses=responses)
    @action(methods=['patch'], detail=True)
    def update_signatures(self, request, pk=None):
        """Обновить настройки подписей."""
        instance = self.get_object()
        signatures = instance.signatures
        return self._update_settings(request, instance, signatures)
