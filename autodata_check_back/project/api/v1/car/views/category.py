from rest_framework import mixins, permissions

from api.v1.car.serializers.category import CategorySerializer
from apps.car.models.category import Category
from apps.helpers.viewsets import ExtendedViewSet


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, ExtendedViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    serializer_class_map = {
        'list': CategorySerializer,
        'retrieve': CategorySerializer,
    }

    permission_classes = (permissions.IsAuthenticated,)
