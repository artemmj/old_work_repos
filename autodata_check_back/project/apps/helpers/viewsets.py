# flake8: noqa
from typing import Type

from django.db.models import Model, Subquery
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


def paginate_response(viewset, queryset=None, serializer_class=None, context=None, add_context=None):
    if queryset is None:
        queryset = viewset.filter_queryset(viewset.get_queryset())

    serializer_class = serializer_class or viewset.get_serializer_class()
    context = context or viewset.get_serializer_context()
    if add_context:
        context.update(add_context)

    page = viewset.paginate_queryset(queryset)
    if page is not None:
        serializer = serializer_class(page, many=True, context=context)
        return viewset.get_paginated_response(serializer.data)

    serializer = serializer_class(queryset, many=True, context=context)
    return Response(serializer.data)


class ExtendViewSet:
    """This viewset mixin class with extended options list."""

    permission_map = {}
    throttle_scope_map = {}
    throttle_class_map = {}
    serializer_class_map = {}

    def get_queryset(self):
        queryset = super().get_queryset()
        serializer_class = self.get_serializer_class()(self.action, self.serializer_class)
        if hasattr(serializer_class, 'setup_eager_loading'):
            queryset = serializer_class.setup_eager_loading(queryset)
        return queryset

    def get_serializer_class(self):
        self.serializer_class = self.serializer_class_map.get(self.action, self.serializer_class)
        return super().get_serializer_class()

    def initialize_request(self, request, *args, **kwargs):
        request = super().initialize_request(request, *args, **kwargs)
        throttle_scope = self.throttle_scope_map.get(self.action, None)
        throttle_class = self.throttle_class_map.get(self.action, None)
        cls_throttle_scope = getattr(self, 'throttle_scope', None)
        cls_throttle = getattr(self, 'throttle_classes', None)
        self.throttle_scope = throttle_scope or cls_throttle_scope or ''
        self.throttle_classes = throttle_class or cls_throttle
        return request

    def get_permissions(self):
        perms = self.permission_map.get(self.action, None)
        if perms and not isinstance(perms, (tuple, list)):
            perms = [perms]
        self.permission_classes = perms or self.permission_classes
        return super().get_permissions()


class ExtendedViewSet(ExtendViewSet, GenericViewSet):
    pass


class ExtendedModelViewSet(ExtendViewSet, viewsets.ModelViewSet):
    """
    Examples:
    class MyModelViewSet(ExtendedModelViewSet):
        serializer_class_map = {
            'list': ListMyModelSerializer,
            'retrieve': RetrieveMyModelSerializer,
            'update': UpdateMyModelSerializer,
            ...
        }
    """

    pass


class SwaggerFriendlyExtendedViewSet(ExtendViewSet, viewsets.GenericViewSet):
    pass


class SwaggerFriendlyExtendedModelViewSet(SwaggerFriendlyExtendedViewSet, viewsets.ModelViewSet):
    pass


class ExtendedGenericViewSet(ExtendViewSet, viewsets.GenericViewSet):
    pass


class RUDExtendedModelViewSet(
    ExtendViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


class RUExtendedModelViewSet(
    ExtendViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    pass

class ReadExtendedModelViewSet(
    ExtendViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    pass


class CRDExtendedModelViewSet(
    ExtendViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


class CRUExtendedModelViewSet(
    ExtendViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    pass


class CRUDExtendedModelViewSet(
    ExtendViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


class ColumnFilterMixin:
    def default_model_column_filter(self, model_class: Type[Model], id_field_name: str, **filter_kwargs):
        """Стандартный умный фильтр по связанной модели.

        :param model_class: модель фильтруемого поля.
        :param id_field_name: имя поля в основной модели.
        :param filter_kwargs: дополнительные параметры фильтрации.
        :return: Response
        """
        main_qs = self.filter_queryset(self.get_queryset())
        ids = main_qs.values(id_field_name).order_by().distinct()
        qs = model_class.objects.filter(id__in=Subquery(ids), **filter_kwargs)
        return paginate_response(self, qs)

    def default_simple_column_filter(self, id_field_name: str):
        """Стандартный умный фильтр по полю.

        :param id_field_name: имя поля в основной модели.
        :return: Response
        """
        main_qs = self.filter_queryset(self.get_queryset())
        qs = main_qs.filter(
            **{
                f'{id_field_name}__isnull': False,
            }
        ).values_list(id_field_name, flat=True).order_by().distinct()
        return paginate_response(self, qs)
