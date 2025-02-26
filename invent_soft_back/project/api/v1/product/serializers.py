from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from api.v1.project.serializers import ProjectListSerializer
from api.v1.zone.serializers import ZoneReadCompactSerializer
from apps.changelog.models import ChangeLog, ChangeLogActionType, ChangeLogModelType
from apps.helpers.serializers import EagerLoadingSerializerMixin
from apps.product.models import AdditionalProductTitleAttribute, FileOfProjectProducts, Product, ScannedProduct
from apps.project.models import Project


class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'vendor_code', 'remainder', 'price', 'am', 'dm')
        read_only_fields = ('id',)

    def update(self, instance, validated_data):
        obj = super().update(instance, validated_data)
        dict_val_data = validated_data.copy()
        dict_val_data['price'] = float(dict_val_data['price'])
        ChangeLog.objects.create(
            project=obj.project,
            model=ChangeLogModelType.PRODUCT,
            record_id=instance.pk,
            action_on_model=ChangeLogActionType.UPDATE,
            changed_data=dict_val_data,
        )
        return obj


class ProductReadSerializer(EagerLoadingSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'vendor_code', 'barcode', 'title', 'remainder', 'price', 'am', 'dm')
        read_only_fields = ('id',)


class ScannedProductSerializer(serializers.ModelSerializer):
    product = ProductReadSerializer()

    class Meta:
        model = ScannedProduct
        fields = ('id', 'created_at', 'scanned_time', 'product', 'amount', 'added_by_product_code', 'dm')


class ScannedProductReadSerializer(serializers.ModelSerializer):
    zone = serializers.SerializerMethodField()
    product = ProductReadSerializer()

    class Meta:
        model = ScannedProduct
        fields = ('id', 'zone', 'product', 'amount', 'added_by_product_code', 'dm')

    @swagger_serializer_method(serializer_or_field=ZoneReadCompactSerializer)
    def get_zone(self, obj):
        return ZoneReadCompactSerializer(obj.task.zone).data


class ScannedProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScannedProduct
        fields = ('amount',)


class GenerateProductsFileSerializer(serializers.Serializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), required=True)


class FileOfProjectProductsSerializer(serializers.ModelSerializer):
    project = ProjectListSerializer()
    products_file = serializers.SerializerMethodField()

    class Meta:
        model = FileOfProjectProducts
        fields = ('id', 'created_at', 'project', 'products_file')

    def get_products_file(self, instance):
        return self.context['request'].build_absolute_uri(instance.products_file)


class AdditionalProductTitleAttrBackupSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='pk')
    product = serializers.CharField(source='product.pk')

    class Meta:
        model = AdditionalProductTitleAttribute
        fields = ('id', 'product', 'content', 'is_hidden')
