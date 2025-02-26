from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.task.filters import TaskFilterSet
from api.v1.task.serializers import TaskReadSerializer
from apps.helpers.exceptions import ErrorResponseSerializer
from apps.helpers.serializers import EnumSerializer
from apps.helpers.viewsets import ListExtendedModelViewSet
from apps.task.models import Task, TaskTypeChoices


class TaskViewSet(ListExtendedModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskReadSerializer
    permission_classes = (permissions.AllowAny,)
    filterset_class = TaskFilterSet

    @swagger_auto_schema(responses={
        200: EnumSerializer(many=True),
        404: ErrorResponseSerializer,
    })
    @action(methods=['get'], detail=False)
    def types_choices(self, request):
        roles = []
        for role in TaskTypeChoices.choices:
            roles.append({'value': role[0], 'name': role[1]})
        return Response(roles)
