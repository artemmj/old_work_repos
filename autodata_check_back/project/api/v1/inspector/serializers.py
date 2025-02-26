from rest_framework import serializers

from apps.inspector.models import Inspector, Requisite


class RequisiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requisite
        fields = (
            'id',
            'created_at',
            'account_number',
            'bank',
            'bik',
            'inn',
            'kpp',
            'correspondent_account',
        )
        read_only_fields = ('id', 'created_at')


class InspectorSerializer(serializers.ModelSerializer):
    requisite = RequisiteSerializer()

    class Meta:
        model = Inspector
        fields = (
            'id',
            'created_at',
            'inn',
            'work_skills',
            'availability_thickness_gauge',
            'radius',
            'balance',
            'requisite',
        )
