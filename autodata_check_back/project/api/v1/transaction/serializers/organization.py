from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from api.v1.organization.serializers import OrganizationReadCompactSerializer
from api.v1.user import UserCompactSerializer
from apps.helpers.serializers import EagerLoadingSerializerMixin, EnumField
from apps.transaction.models import OrganizationTransaction, OrganizationTransactionOperations
from apps.transaction.models.abstract import TransactionStatuses, TransactionTypes


class OrganizationTransactionReadSerializer(EagerLoadingSerializerMixin, serializers.ModelSerializer):
    status = EnumField(enum_class=TransactionStatuses)
    type = EnumField(enum_class=TransactionTypes)
    operation = EnumField(enum_class=OrganizationTransactionOperations)
    organization = OrganizationReadCompactSerializer()
    user = UserCompactSerializer()

    select_related_fields = ('organization', 'user', 'user__avatar')

    class Meta:
        model = OrganizationTransaction
        fields = ('id', 'created_at', 'status', 'type', 'operation', 'amount', 'organization', 'user')
        read_only_fields = ('id', 'created_at')


class OrganizationTransactionBalanceReplenishmentSerializer(OrganizationTransactionReadSerializer):  # noqa: WPS118
    payment_url = serializers.SerializerMethodField(help_text='URL адрес страницы оплаты')
    status = serializers.ChoiceField(choices=TransactionStatuses.choices)
    type = serializers.ChoiceField(choices=TransactionTypes.choices)
    operation = serializers.ChoiceField(choices=OrganizationTransactionOperations.choices)

    class Meta:
        model = OrganizationTransaction
        fields = (
            'id',
            'created_at',
            'status',
            'type',
            'operation',
            'amount',
            'organization',
            'user',
            'payment_url',
        )
        read_only_fields = ('id', 'created_at')

    def get_payment_url(self, obj) -> str:
        return obj.payment_url


class OrganizationTransactionRequestSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=CurrentUserDefault())

    class Meta:
        model = OrganizationTransaction
        fields = ('amount', 'organization', 'user')


class OrganizationTransactionCreateSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default=TransactionTypes.ADD)
    operation = serializers.CharField(default=OrganizationTransactionOperations.BALANCE_REPLENISHMENT)
    user = serializers.HiddenField(default=CurrentUserDefault())

    class Meta:
        model = OrganizationTransaction
        fields = ('id', 'created_at', 'status', 'type', 'operation', 'amount', 'organization', 'user')
        read_only_fields = ('id', 'created_at')
