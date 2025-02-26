from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.arketa.clients import ArketaServiceApiClient, ArketaTaskApiClient
from apps.document.services import ValidateCheckDocumentService
from apps.helpers.exceptions import ErrorResponseSerializer
from apps.helpers.serializers import EmptySerializer
from apps.user.permissions import IsApplicantConfirmedPermission, IsApplicantPermission, IsMasterPermission

from ..serializers import (  # noqa: F401 WPS235
    CheckDocResponseSerializer,
    DocumentAllArketaSerializer,
    TaskArketaAnswerWriteRequestSerializer,
    TaskArketaCancelReservationSerializer,
    TaskArketaCurrentQuerySerializer,
    TaskArketaMobileSerializer,
    TaskArketaReserveCounterSerializer,
    TaskArketaStatusesSerializer,
    TaskArketaTakeSerializer,
    TaskArketaVacantQuerySerializer,
    TaskArketaVacantSerializer,
    VisitArketaResponseSerializer,
    VisitArketaSerializer,
)


class ArketaTaskViewSet(ViewSet):  # noqa: WPS214
    permission_classes = (IsApplicantConfirmedPermission | IsApplicantPermission | IsMasterPermission,)

    @swagger_auto_schema(
        operation_summary='Список задач доступных для бронирования.',
        query_serializer=TaskArketaVacantQuerySerializer(),
        responses={
            status.HTTP_200_OK: TaskArketaVacantSerializer(many=True),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        })
    @action(methods=['get'], detail=False)
    def vacant(self, request):
        serializer = TaskArketaVacantQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        token = request.META.get('HTTP_AUTHORIZATION')
        return Response(ArketaTaskApiClient(token).task_vacant(serializer.data))

    @swagger_auto_schema(
        operation_summary='Счетчик количества забронированных задач у пользователя.',
        responses={
            status.HTTP_200_OK: TaskArketaReserveCounterSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        })
    @action(methods=['get'], detail=False)
    def available_for_reserve(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        return Response(ArketaTaskApiClient(token).task_available_for_reserve())

    @swagger_auto_schema(
        operation_summary='Просмотр задачи перед бронированием.',
        responses={
            status.HTTP_200_OK: TaskArketaMobileSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        })
    @action(methods=['get'], detail=False, url_path=r'(?P<task_id>[\w-]+)/preview')
    def preview(self, request, task_id=None):
        token = request.META.get('HTTP_AUTHORIZATION')
        return Response(ArketaTaskApiClient(token).task_preview(task_id))

    @swagger_auto_schema(
        operation_summary='Бронирование/взятие задач исполнителем.',
        request_body=TaskArketaTakeSerializer(),
        responses={
            status.HTTP_200_OK: TaskArketaTakeSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        })
    @action(methods=['post'], detail=False, url_path='vacant/take')
    def vacant_take(self, request):
        serializer = TaskArketaTakeSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        tasks = serializer.validated_data['tasks']
        collection = serializer.validated_data.get('collection')
        token = request.META.get('HTTP_AUTHORIZATION')
        return Response(ArketaTaskApiClient(token).vacant_take(tasks, collection))

    @swagger_auto_schema(
        operation_summary='Проверка наличия юзера и документов.',
        responses={
            status.HTTP_200_OK: CheckDocResponseSerializer(many=True),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        })
    @action(['get'], detail=False)
    def check_docs(self, request):
        """Проверить документы в работуте и аркете."""
        return Response(ValidateCheckDocumentService(request).process())

    @swagger_auto_schema(
        operation_summary='Получить статусы всех документов пользователя.',
        responses={
            status.HTTP_200_OK: DocumentAllArketaSerializer(many=True),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        })
    @action(['get'], detail=False, url_path=r'documents/user/(?P<user_id>[\w-]+)/documents')
    def documents(self, request, user_id: str):
        return Response(ArketaServiceApiClient().get_documents(self.request.user.pk))

    @swagger_auto_schema(
        operation_summary='Список кол-ва задач разбитых по статусам.',
        responses={
            status.HTTP_200_OK: TaskArketaStatusesSerializer(many=True),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        })
    @action(['get'], detail=False)
    def statuses(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        return Response(ArketaTaskApiClient(token).statuses())

    @swagger_auto_schema(
        operation_summary='Задачи пользователя.',
        query_serializer=TaskArketaCurrentQuerySerializer(),
        responses={
            status.HTTP_200_OK: TaskArketaMobileSerializer(many=True),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        })
    @action(['get'], detail=False)
    def current(self, request):
        serializer = TaskArketaCurrentQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        token = request.META.get('HTTP_AUTHORIZATION')
        service_result = ArketaTaskApiClient(token).current(serializer.data)
        return Response(service_result.get('results'))

    @swagger_auto_schema(
        operation_summary='Отмена бронирования/отказ от задачи.',
        request_body=TaskArketaCancelReservationSerializer(),
        responses={
            status.HTTP_200_OK: TaskArketaCancelReservationSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        })
    @action(['post'], detail=False, url_path=r'(?P<task_id>[\w-]+)/cancel_reservation')
    def cancel_reservation(self, request, task_id=None):
        serializer = TaskArketaCancelReservationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = request.META.get('HTTP_AUTHORIZATION')
        return Response(ArketaTaskApiClient(token).cancel_reservation(task_id, serializer.data))

    @swagger_auto_schema(
        operation_summary='Отправка ответов.',
        request_body=TaskArketaAnswerWriteRequestSerializer(),
        responses={
            status.HTTP_200_OK: TaskArketaAnswerWriteRequestSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        })
    @action(['post'], detail=False)
    def answer(self, request):
        serializer = TaskArketaAnswerWriteRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = request.META.get('HTTP_AUTHORIZATION')
        return Response(ArketaTaskApiClient(token).answer(serializer.data))

    @swagger_auto_schema(
        operation_summary='Фиксация визита.',
        request_body=VisitArketaSerializer(),
        responses={
            status.HTTP_200_OK: VisitArketaResponseSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        })
    @action(['post'], detail=False)
    def visit(self, request):
        serializer = VisitArketaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = request.META.get('HTTP_AUTHORIZATION')
        return Response(ArketaTaskApiClient(token).visit(serializer.data))

    @swagger_auto_schema(
        operation_summary='Добавить задачу в избранное.',
        responses={
            status.HTTP_200_OK: EmptySerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        })
    @action(['post'], detail=False, url_path=r'(?P<task_id>[\w-]+)/like')
    def like(self, request, task_id):
        token = request.META.get('HTTP_AUTHORIZATION')
        return Response(ArketaTaskApiClient(token).like(task_id))

    @swagger_auto_schema(
        operation_summary='Удалить задачу из избранного.',
        responses={
            status.HTTP_200_OK: EmptySerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        })
    @action(['post'], detail=False, url_path=r'(?P<task_id>[\w-]+)/dislike')
    def dislike(self, request, task_id):
        token = request.META.get('HTTP_AUTHORIZATION')
        return Response(ArketaTaskApiClient(token).dislike(task_id))
