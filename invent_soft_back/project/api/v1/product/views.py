from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from api.v1.product.filters import ProductFilterSet, ScannedProductFilterSet
from api.v1.product.serializers import (
    FileOfProjectProductsSerializer,
    ProductReadSerializer,
    ProductUpdateSerializer,
    ScannedProductReadSerializer,
    ScannedProductUpdateSerializer,
)
from api.v1.product.services import AmountUpdateService
from apps.helpers.pagination import ServerTimePagination
from apps.helpers.viewsets import ListRetrieveUpdateExtendedModelViewSet, ListUpdateExtendedModelViewSet
from apps.product.models import FileOfProjectProducts, Product, ScannedProduct


class ProductViewSet(ListUpdateExtendedModelViewSet):
    queryset = Product.objects.all().exclude(title='Неизвестный товар')
    serializer_class = ProductUpdateSerializer
    serializer_class_map = {
        'list': ProductReadSerializer,
    }
    permission_classes = (permissions.AllowAny,)
    search_fields = ('vendor_code', 'barcode', 'zone__title')
    ordering_fields = ('vendor_code', 'barcode', 'title', 'remainder', 'price', 'zone__title', 'zone__storage_name')
    filterset_class = ProductFilterSet
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    pagination_class = ServerTimePagination

    @swagger_auto_schema(responses={200: FileOfProjectProductsSerializer(many=True)})
    @action(['GET'], detail=False, url_path='get-products-files', url_name='products_get-products-files')
    def get_products_files(self, request):
        serializer = FileOfProjectProductsSerializer(
            FileOfProjectProducts.objects.all(),
            context={'request': request},
            many=True,
        )
        return Response(serializer.data)


class ScannedProductViewSet(ListRetrieveUpdateExtendedModelViewSet):
    queryset = ScannedProduct.objects.all().order_by('-created_at')
    serializer_class = ScannedProductReadSerializer
    permission_classes = (permissions.IsAuthenticated,)
    search_fields = ('product__vendor_code', 'product__barcode')
    ordering_fields = ('product__vendor_code', 'product__barcode', 'product__title', 'task__zone__title', 'amount')
    filterset_class = ScannedProductFilterSet
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)

    def partial_update(self, request, pk=None):
        serializer = ScannedProductUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sсan_prd = ScannedProduct.objects.get(pk=pk)  # noqa: WPS119
        service_res = AmountUpdateService(sсan_prd, serializer.data).process()
        return Response(ScannedProductReadSerializer(service_res).data)
