from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from api.v1.stories.serializers.stories_mailing import (
    BaseStoriesMailingListSerializer,
    StoriesMailingPolymorphicSerializer,
    StoriesMailingRetrievePolymorphicSerializer,
    StoriesMailingRetrieveSwaggerSerializer,
    StoriesMailingSwaggerSerializer,
    StoriesMailingUpdateSwaggerSerializer,
)
from apps.helpers.exceptions import ErrorResponseSerializer
from apps.helpers.viewsets import ExtendedModelViewSet
from apps.stories.models import BaseStoriesMailing
from apps.user.permissions import IsMasterPermission


class StoriesMailingViewSet(ExtendedModelViewSet):
    queryset = BaseStoriesMailing.objects.filter(
        stories__deleted_at__isnull=True,
    ).order_by('-stories__is_top', '-created_at')
    serializer_class = StoriesMailingPolymorphicSerializer
    serializer_class_map = {
        'list': BaseStoriesMailingListSerializer,
        'retrieve': StoriesMailingRetrievePolymorphicSerializer,
    }
    search_fields = ('stories__name',)
    ordering_fields = ('publish_datetime',)
    filter_backends = (SearchFilter, OrderingFilter)
    permission_classes = (IsMasterPermission,)
    http_method_names = ('get', 'post', 'patch')

    @swagger_auto_schema(
        request_body=no_body,
        responses={
            status.HTTP_200_OK: StoriesMailingRetrieveSwaggerSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(self, request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=StoriesMailingSwaggerSerializer(),
        responses={
            status.HTTP_201_CREATED: StoriesMailingRetrieveSwaggerSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            StoriesMailingRetrievePolymorphicSerializer(instance, context=self.get_serializer_context()).data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    @swagger_auto_schema(
        request_body=StoriesMailingUpdateSwaggerSerializer(),
        responses={
            status.HTTP_200_OK: StoriesMailingRetrieveSwaggerSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    def partial_update(self, request, *args, **kwargs):
        super().partial_update(request, *args, **kwargs)
        instance = self.get_object()
        return Response(
            StoriesMailingRetrievePolymorphicSerializer(
                instance,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_200_OK,
        )
