from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action

from api.v1.changelog.filters import ChangeLogFilterSet
from api.v1.changelog.serializers import ChangeLogDeletedProductsSerializer, ChangeLogSerializer
from apps.changelog.models import ChangeLog, ChangeLogActionType, ChangeLogModelType
from apps.helpers.pagination import ServerTimePagination
from apps.helpers.viewsets import ListRetrieveModelViewSet, paginate_response


class ChangeLogViewSet(ListRetrieveModelViewSet):
    queryset = ChangeLog.objects.all()
    serializer_class = ChangeLogSerializer
    filterset_class = ChangeLogFilterSet
    pagination_class = ServerTimePagination

    @swagger_auto_schema(method='get', responses={200: ChangeLogDeletedProductsSerializer(many=True)})
    @action(['get'], detail=False, url_path='deleted-products', url_name='change-log-deleted-products')
    def deleted_products(self, request):
        queryset = ChangeLog.objects.filter(
            action_on_model=ChangeLogActionType.DELETE,
            model=ChangeLogModelType.PRODUCT,
        )
        queryset = self.filter_queryset(queryset)
        return paginate_response(self, queryset, ChangeLogDeletedProductsSerializer)
