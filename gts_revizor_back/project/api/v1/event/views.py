from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.filters import OrderingFilter, SearchFilter

from api.v1.event.serializers import EventSerializer
from apps.event.models import Event
from apps.helpers.viewsets import ListRetrieveModelViewSet

from .filters import EventFilterSet


class EventViewSet(ListRetrieveModelViewSet):
    queryset = Event.objects.all().order_by('-fake_id')
    serializer_class = EventSerializer
    serializer_class_map = {
        'list': EventSerializer,
    }
    permission_classes = (permissions.IsAuthenticated,)
    search_fields = ('title',)
    ordering_fields = ('id', 'created_at', 'title', 'fake_id')
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = EventFilterSet
