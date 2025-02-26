from django.core.files.storage import default_storage
from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.city.serializers import CityReadSerializer, CityWriteSerializer, ImportExcelRequestSerializer
from apps.address.models import City
from apps.address.tasks import cities_export_excel, cities_import_excel
from apps.helpers.celery import CeleryResultSerializer
from apps.helpers.viewsets import RUExtendedModelViewSet


class CityViewSet(RUExtendedModelViewSet):
    queryset = City.objects.all()
    serializer_class = CityReadSerializer
    serializer_class_map = {
        'update': CityWriteSerializer,
        'partial_update': CityWriteSerializer,
        'import_excel': ImportExcelRequestSerializer,
    }
    search_fields = ('title', 'inspection_price')
    ordering_fields = ('title', 'inspection_price')

    @swagger_auto_schema(request_body=no_body, responses={200: CeleryResultSerializer})
    @action(methods=['post'], detail=False)
    def export_excel(self, request):
        host = f'{request.scheme}://{request.get_host()}'
        task = cities_export_excel.delay(host)
        return Response({'result_id': task.id}, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=ImportExcelRequestSerializer, responses={200: CeleryResultSerializer})
    @action(methods=['post'], detail=False)
    def import_excel(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = request.FILES['file']
        file_name = default_storage.save(file.name, file)
        task = cities_import_excel.delay(file=file_name)
        return Response({'result_id': task.id}, status=status.HTTP_200_OK)
