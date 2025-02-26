from rest_framework import serializers

from apps.helpers.serializers import EnumField
from apps.transaction.models import InspectorTransaction, InspectorTransactionOperations
from apps.transaction.models.abstract import TransactionStatuses, TransactionTypes


class InspectorTransactionReadSerializer(serializers.ModelSerializer):
    status = EnumField(enum_class=TransactionStatuses)
    type = EnumField(enum_class=TransactionTypes)
    operation = EnumField(enum_class=InspectorTransactionOperations)

    class Meta:
        model = InspectorTransaction
        fields = ('id', 'created_at', 'status', 'type', 'operation', 'amount', 'inspector')
        read_only_fields = ('id', 'created_at')
