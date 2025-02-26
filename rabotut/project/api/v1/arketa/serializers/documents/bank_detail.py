from rest_framework import serializers


class BankDetailSerializer(serializers.Serializer):
    bank_account = serializers.CharField()
    bik = serializers.CharField()
    document_status = serializers.CharField()
