from rest_framework import serializers

from apps.changelog.models import ChangeLog


class ChangeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangeLog
        fields = (
            'id',
            'created_at',
            'project',
            'model',
            'record_id',
            'action_on_model',
            'changed_data',
        )


class ChangeLogDeletedProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangeLog
        fields = (
            'record_id',
        )
