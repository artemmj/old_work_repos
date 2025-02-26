from rest_framework import serializers

from .brand import BrandSerializer
from .file import FileArketaSerializer
from .trade_network import TradeNetworkReadSerializer


class VacantTaskSKUSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    created_at = serializers.DateTimeField()
    name = serializers.CharField()
    barcode = serializers.CharField()
    brand = BrandSerializer()
    images = FileArketaSerializer(many=True)


class CompanyCompactSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()


class PLUCompactSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    code = serializers.CharField()
    network = TradeNetworkReadSerializer()


class CategorySerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()


class SubCategorySerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    category = serializers.UUIDField()


class GroupSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()


class SubBrandSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    brand = serializers.UUIDField()


class SKUReadSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=False)
    created_at = serializers.DateTimeField(required=False)
    name = serializers.CharField()
    barcode = serializers.CharField(required=False)
    plues = PLUCompactSerializer(many=True)
    ean = serializers.ListField(child=serializers.CharField(), required=False)
    brand = BrandSerializer()
    subbrand = SubBrandSerializer()
    category = CategorySerializer()
    subcategory = SubCategorySerializer()
    group = GroupSerializer()
    client_code = serializers.CharField(required=False)
    is_new = serializers.BooleanField(required=False)
    images = FileArketaSerializer(many=True)
    company = CompanyCompactSerializer()
