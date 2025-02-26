from django_filters import CharFilter, FilterSet, NumberFilter, UUIDFilter

from apps.product.models import Product, ScannedProduct


class ProductFilterSet(FilterSet):
    project = UUIDFilter(field_name='project', required=True)
    vendor_code = CharFilter(field_name='vendor_code', lookup_expr='icontains')
    barcode = CharFilter(field_name='barcode', lookup_expr='icontains')
    title = CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ('project',)


class ScannedProductFilterSet(FilterSet):
    project = UUIDFilter(field_name='task__zone__project', required=True)
    vendor_code = CharFilter(field_name='product__vendor_code', lookup_expr='icontains')
    barcode = CharFilter(field_name='product__barcode', lookup_expr='icontains')
    zone_number_start = NumberFilter(field_name='task__zone__serial_number', lookup_expr='gte')
    zone_number_end = NumberFilter(field_name='task__zone__serial_number', lookup_expr='lte')

    class Meta:
        model = ScannedProduct
        fields = ('project',)
