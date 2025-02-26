from django.db.models import Q  # noqa: WPS201 WPS347
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from apps.helpers.celery import CeleryResultSerializer
from apps.helpers.exceptions import ErrorResponseSerializer
from apps.helpers.serializers import EmptySerializer
from apps.helpers.viewsets import ExtendedModelViewSet, paginate_response
from apps.survey.models import (
    Survey,
    SurveyMailingDepartments,
    SurveyMailingProjects,
    SurveyMailingRegions,
    SurveyMailingRoles,
)
from apps.survey.services import DeleteListSurveyService, SendSurveyReplyService
from apps.survey.tasks import generate_survey_report
from apps.user.permissions import IsApplicantConfirmedPermission, IsApplicantPermission, IsMasterPermission

from ..filters import SurveyFilterSet
from ..serializers import (  # noqa: WPS235
    AnswerSerializer,
    SendSurveyReplySerializer,
    SurveyCreateSerializer,
    SurveyListIdSerializer,
    SurveyMobileRetrieveSerializer,
    SurveyMobileSerializer,
    SurveyRetrieveSerializer,
    SurveySerializer,
    SurveyUpdateSerializer,
)


class SurveyViewSet(ExtendedModelViewSet):  # noqa: WPS214
    queryset = Survey.objects.non_deleted()
    serializer_class = SurveySerializer
    serializer_class_map = {
        'retrieve': SurveyRetrieveSerializer,
        'create': SurveyCreateSerializer,
        'partial_update': SurveyUpdateSerializer,
        'delete_list_surveys': SurveyListIdSerializer,
        'surveys_mobile': SurveyMobileSerializer,
        'surveys_mobile_retrieve': SurveyMobileRetrieveSerializer,
        'send_reply': SendSurveyReplySerializer,
    }
    permission_classes = (IsMasterPermission | IsApplicantPermission | IsApplicantConfirmedPermission,)
    permission_map = {
        'list': IsMasterPermission,
        'retrieve': IsMasterPermission,
        'create': IsMasterPermission,
        'partial_update': IsMasterPermission,
        'delete_list_surveys': IsMasterPermission,
        'survey_report': IsMasterPermission,
        'surveys_mobile': (IsApplicantPermission | IsApplicantConfirmedPermission,),
        'surveys_mobile_retrieve': (IsApplicantPermission | IsApplicantConfirmedPermission,),
        'send_reply': (IsApplicantPermission | IsApplicantConfirmedPermission,),
    }
    filterset_class = SurveyFilterSet
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    ordering_fields = ('mailings__publish_datetime', 'is_self_option')
    http_method_names = ('get', 'post', 'patch')

    def get_queryset(self):
        queryset = super().get_queryset()
        if IsMasterPermission().has_permission(self.request, self):
            return queryset.order_by('-created_at')
        if (IsApplicantPermission | IsApplicantConfirmedPermission)().has_permission(self.request, self):
            user = self.request.user
            # Исключить опросы, которые юзер уже прошел
            queryset = queryset.exclude(questions__answer__user=user)
            mailing_departments = SurveyMailingDepartments.objects.filter(departments=user.department)
            mailing_regions = SurveyMailingRegions.objects.filter(regions__in=user.regions.all())
            mailing_projects = SurveyMailingProjects.objects.filter(projects__in=user.projects.all())
            mailing_user_roles = SurveyMailingRoles.objects.filter(roles__contains=[user.role])
            queryset = queryset.filter(
                Q(mailings__in=mailing_departments)
                | Q(mailings__in=mailing_regions)
                | Q(mailings__in=mailing_projects)
                | Q(mailings__in=mailing_user_roles),
            ).distinct()
            return queryset.order_by('-created_at')
        return queryset.none()

    @swagger_auto_schema(
        operation_summary='Создать опрос.',
        request_body=SurveyCreateSerializer(),
        responses={
            status.HTTP_201_CREATED: SurveyRetrieveSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(SurveyRetrieveSerializer(instance).data, status=status.HTTP_201_CREATED, headers=headers)

    @swagger_auto_schema(
        operation_summary='Обновить опрос.',
        request_body=SurveyCreateSerializer(),
        responses={
            status.HTTP_200_OK: SurveyRetrieveSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    def partial_update(self, request, *args, **kwargs):
        super().partial_update(request, *args, **kwargs)
        instance = self.get_object()
        return Response(SurveyRetrieveSerializer(instance).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Удалить список опросов.',
        request_body=SurveyListIdSerializer(),
        responses={
            status.HTTP_204_NO_CONTENT: EmptySerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    @action(methods=['post'], detail=False)
    def delete_list_surveys(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        surveys_ids = serializer.validated_data.get('surveys_ids')
        DeleteListSurveyService(surveys_ids=surveys_ids).process()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        operation_summary='Отчет по опросу.',
        request_body=EmptySerializer(),
        responses={
            status.HTTP_204_NO_CONTENT: CeleryResultSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    @action(methods=['POST'], detail=True)
    def survey_report(self, request, pk=None):
        task = generate_survey_report.delay(survey_id=self.get_object().pk)
        return Response({'result_id': task.id})

    @swagger_auto_schema(
        operation_summary='Список опросов для мобильного приложения.',
        responses={
            status.HTTP_200_OK: SurveyMobileSerializer(many=True),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    @action(methods=['get'], detail=False, url_path='surveys_mobile')
    def surveys_mobile(self, request, pk=None):
        queryset = self.filter_queryset(self.get_queryset())
        return paginate_response(self, queryset)

    @swagger_auto_schema(
        operation_summary='Деталка опросов для мобильного приложения.',
        responses={
            status.HTTP_200_OK: SurveyMobileRetrieveSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    @action(methods=['get'], detail=True, url_path='surveys_mobile_retrieve')
    def surveys_mobile_retrieve(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Отправить ответ на опрос.',
        responses={
            status.HTTP_200_OK: EmptySerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    @action(methods=['POST'], detail=True)
    def send_reply(self, request, pk=None):
        context = self.get_serializer_context()
        context['survey'] = self.get_object()
        serializer = self.get_serializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        answers = SendSurveyReplyService().process(serializer.validated_data.get('answers'))
        return Response(AnswerSerializer(answers, many=True).data, status=status.HTTP_200_OK)
