from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from api.v1.project.serializers import (  # noqa: WPS235
    CheckPasswordProjectRequestSerializer,
    CheckPasswordProjectResponseSerializer,
    DeleteProductSerializer,
    ExportDocumentSerializer,
    ImportProductSerializer,
    ImportProjectSerializer,
    ImportProjectSettingsSerializer,
    ProjectListSerializer,
    ProjectRetrieveSerializer,
    ProjectWriteSerializer,
)
from apps.event.models import Event
from apps.helpers.batchmixin import DeleteBatchMixin
from apps.helpers.celery import CeleryResultSerializer, CeleryTaskWrapper
from apps.helpers.exceptions import ErrorResponseSerializer
from apps.helpers.viewsets import ExtendedModelViewSet
from apps.product.models import Product
from apps.project.models import Project
from apps.project.services.check_password import ProjectCheckPasswordService
from apps.project.tasks import (  # noqa: WPS235
    delete_products_celery_wrapper,
    export_document_celery_wrapper,
    export_project_new_celery_task_wrapper,
    export_settings,
    import_employees_celery_wrapper,
    import_products_celery_wrapper,
    import_project_new_celery_task_wrapper,
    import_settings,
    import_zones_celery_wrapper,
)
from apps.task.models import Task
from apps.template.models import Template


class ProjectViewSet(ExtendedModelViewSet, DeleteBatchMixin):  # noqa: WPS214
    queryset = Project.objects.all()
    serializer_class = ProjectWriteSerializer
    serializer_class_map = {
        'list': ProjectListSerializer,
        'retrieve': ProjectRetrieveSerializer,
    }
    permission_classes = (permissions.IsAuthenticated,)
    permission_map = {
        'list': permissions.AllowAny,
        'retrieve': permissions.AllowAny,
    }
    search_fields = ('title',)
    ordering_fields = ('title', 'created_at', 'address')
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)

    def destroy(self, request, pk=None):
        instance = self.get_object()
        Task.objects.filter(zone__project=instance).delete()
        Event.objects.filter(project=instance).delete()
        instance.rmm_settings.delete()
        instance.terminal_settings.delete()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        request_body=CheckPasswordProjectRequestSerializer,
        responses={200: CheckPasswordProjectResponseSerializer, 404: ErrorResponseSerializer},
    )
    @action(methods=['post'], detail=True)
    def check_password(self, request, pk=None):
        """Проверка пароля проекта."""
        project = self.get_object()
        password = request.data['password']
        result = ProjectCheckPasswordService().process(project, password)
        serializer = CheckPasswordProjectResponseSerializer({'result': result})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=ImportProjectSettingsSerializer, responses={200: CeleryResultSerializer})
    @action(methods=['post'], detail=False)
    def import_settings(self, request):
        """Загрузка файла с настройками проекта."""
        task = CeleryTaskWrapper(ImportProjectSettingsSerializer, import_settings)
        return Response({'result_id': task.execute(request)}, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=no_body, responses={200: CeleryResultSerializer})
    @action(methods=['post'], detail=True)
    def export_settings(self, request, pk=None):
        """Выгрузка файла с настройками проекта."""
        host = f'{request.scheme}://{request.get_host()}'
        task = export_settings.delay(pk, host)
        return Response({'result_id': task.id}, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=ImportProductSerializer, responses={200: CeleryResultSerializer})
    @action(methods=['post'], detail=False)
    def import_products(self, request):
        """Загрузка cправочника с продуктами или зонами или сотрудниками."""
        serializer = ImportProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        template = Template.objects.get(pk=serializer.data['template'])

        if 'zone_code' in template.fields or 'zone_name' in template.fields or 'storage_code' in template.fields:
            task = import_zones_celery_wrapper.delay(serializer.data)
        elif 'serial_number' in template.fields and 'full_name' in template.fields:
            task = import_employees_celery_wrapper.delay(serializer.data)
        else:
            task = import_products_celery_wrapper.delay(serializer.data)

        return Response({'result_id': task.id}, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    @swagger_auto_schema(request_body=DeleteProductSerializer, responses={200: CeleryResultSerializer})
    @action(methods=['post'], detail=False)
    def delete_products(self, request):  # noqa: WPS231
        """Удаление cправочника с продуктами."""
        serializer = DeleteProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = serializer.data.get('project')  # noqa: DAR401
        if not Product.objects.filter(project__pk=project).exclude(title='Неизвестный товар').count():
            raise ValidationError('Параметров справочника нет в системе')
        if 'delete_all' not in serializer.data.get('params'):
            if 'delete_prices' in serializer.data.get('params'):
                null_prices = set(list(  # noqa: C414
                    Product.objects.filter(
                        project__pk=project,
                    ).values_list('price', flat=True),
                ))
                if len(null_prices) == 1 and null_prices.pop() == 0:
                    raise ValidationError('Параметра цены нет в системе')
            if 'delete_remainders' in serializer.data.get('params'):
                null_remainders = set(list(  # noqa: C414
                    Product.objects.filter(
                        project__pk=project,
                    ).values_list('remainder', flat=True),
                ))
                if len(null_remainders) == 1 and null_remainders.pop() == 0:
                    raise ValidationError('Параметра остатков нет в системе')
        task = delete_products_celery_wrapper.delay(serializer.data)
        return Response({'result_id': task.id}, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=ExportDocumentSerializer, responses={200: CeleryResultSerializer})
    @action(methods=['post'], detail=False)
    def export_document(self, request):
        """Выгрузка файла по шаблону."""
        serializer = ExportDocumentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = export_document_celery_wrapper.delay(
            project_id=serializer.data['project'],
            template_id=serializer.data['template'],
            export_file_format=serializer.data['format'],
        )
        return Response({'result_id': task.id}, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=no_body, responses={200: CeleryResultSerializer})
    @action(methods=['post'], detail=True)
    def export_project(self, request, pk=None):
        """Выгрузка файла со всеми настройками проекта."""
        host = f'{request.scheme}://{request.get_host()}'
        task = export_project_new_celery_task_wrapper.delay(host, pk)
        return Response({'result_id': task.id}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ImportProjectSerializer, responses={200: CeleryResultSerializer},
    )
    @action(methods=['post'], detail=False)
    def import_project(self, request):
        """Загрузка файла с настройками проекта."""
        serializer = ImportProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = import_project_new_celery_task_wrapper.delay(serializer.data['file'])
        return Response({'result_id': task.id})
