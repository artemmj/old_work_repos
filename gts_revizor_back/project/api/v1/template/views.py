from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.template.filters import TemplateFieldFilter
from api.v1.template.serializers import (  # noqa: WPS235
    ImportTemplateSerializer,
    TemplateExportFieldsResponseSerializer,
    TemplateExportReadSerializer,
    TemplateExportRequestSerializer,
    TemplateExportWriteSerializer,
    TemplateFieldResponseSerializer,
    TemplateReadSerializer,
    TemplateRetrieveResponseSerializer,
    TemplateWriteSerializer,
)
from apps.event.models import Event, TitleChoices
from apps.helpers.celery import CeleryResultSerializer
from apps.helpers.exceptions import ErrorResponseSerializer
from apps.helpers.serializers import EnumSerializer
from apps.helpers.viewsets import CRUDExtendedModelViewSet
from apps.project.models import Project
from apps.template.models import Template, TemplateExport, TemplateFieldChoices
from apps.template.services.copy_template_fields_to_db import CopyTemplateFieldsToDbService
from apps.template.services.get_unique_template_fields import GetUniqueTemplateFieldsService
from apps.template.tasks import export_template, import_template_exp_celery_wrapper, import_template_imp_celery_wrapper


class TemplateViewSet(CRUDExtendedModelViewSet):
    queryset = Template.objects.all()
    serializer_class = TemplateWriteSerializer
    serializer_class_map = {
        'list': TemplateReadSerializer,
        'retrieve': TemplateRetrieveResponseSerializer,
    }
    permission_classes = (permissions.IsAuthenticated,)

    def destroy(self, request, pk=None):
        template = self.get_object()
        project = Project.objects.filter(template=template)
        Event.objects.create(
            project=project[0] if project else None,
            title=TitleChoices.TEMPLATE_DELETE,
            comment=f'Удален шаблон загрузки {template.title}',
        )
        return super().destroy(request, pk=pk)

    @swagger_auto_schema(responses={
        200: TemplateFieldResponseSerializer(many=True),
        404: ErrorResponseSerializer,
    })
    @action(methods=['get'], detail=False)
    def fields_choices(self, request):
        CopyTemplateFieldsToDbService(template_fields=TemplateFieldChoices.choices).process()
        template_fields = GetUniqueTemplateFieldsService().process()
        filtered_fields = TemplateFieldFilter(request.GET, queryset=template_fields).qs
        return Response(TemplateFieldResponseSerializer(filtered_fields, many=True).data)

    @swagger_auto_schema(
        request_body=ImportTemplateSerializer, responses={200: CeleryResultSerializer},
    )
    @action(methods=['post'], detail=False)
    def import_template(self, request):
        """Загрузка шаблона из файла."""
        serializer = ImportTemplateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = import_template_imp_celery_wrapper.delay(serializer.data['file'])
        return Response({'result_id': task.id}, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=no_body, responses={200: CeleryResultSerializer})
    @action(methods=['post'], detail=True, url_path='export_to_file')
    def export_template(self, request, pk=None):
        """Выгрузка шаблона в файл"""
        host = f'{request.scheme}://{request.get_host()}'
        task = export_template.delay(pk, host, 'template')
        return Response({'result_id': task.id}, status=status.HTTP_200_OK)


class TemplateExportViewSet(CRUDExtendedModelViewSet):
    queryset = TemplateExport.objects.all()
    serializer_class = TemplateExportWriteSerializer
    serializer_class_map = {
        'list': TemplateExportReadSerializer,
        'retrieve': TemplateExportReadSerializer,
    }
    permission_classes = (permissions.IsAuthenticated,)

    def destroy(self, request, pk=None):
        template = self.get_object()
        project = Project.objects.filter(template_export=template)
        Event.objects.create(
            project=project[0] if project else None,
            title=TitleChoices.TEMPLATE_DELETE,
            comment=f'Удален шаблон выгрузки {template.title}',
        )
        return super().destroy(request, pk=pk)

    @swagger_auto_schema(
        query_serializer=TemplateExportRequestSerializer,
        responses={
            200: EnumSerializer(many=True),
            404: ErrorResponseSerializer,
        },
    )
    @action(methods=['get'], detail=False)
    def fields_choices(self, request):
        serializer = TemplateExportRequestSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        template = serializer.validated_data.get('upload_template_id')

        uniq_template_export_fields = [
            'count',
            'discrepancy',
            'discrepancy_decimal',
            'zone_number',
            'zone_name',
            'data_matrix_code',
            'remainder_2',
            'storage_code',
            'terminal',
        ]
        template.fields.extend(uniq_template_export_fields)

        return Response(TemplateExportFieldsResponseSerializer(template).data)

    @swagger_auto_schema(
        request_body=ImportTemplateSerializer, responses={200: CeleryResultSerializer},
    )
    @action(methods=['post'], detail=False)
    def import_template(self, request):
        """Загрузка шаблона из файла."""
        serializer = ImportTemplateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = import_template_exp_celery_wrapper.delay(serializer.data['file'])
        return Response({'result_id': task.id}, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=no_body, responses={200: CeleryResultSerializer})
    @action(methods=['post'], detail=True, url_path='export_to_file')
    def export_template(self, request, pk=None):
        """Выгрузка шаблона в файл"""
        host = f'{request.scheme}://{request.get_host()}'
        task = export_template.delay(pk, host, 'export_template')
        return Response({'result_id': task.id}, status=status.HTTP_200_OK)
