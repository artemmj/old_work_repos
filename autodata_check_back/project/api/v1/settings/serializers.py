from rest_framework import serializers


class SettingsSerializer(serializers.Serializer):
    key = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()  # noqa: WPS110

    def get_key(self, settings):
        return settings[0]

    def get_value(self, settings):
        return settings[1]


class SelfInspectionPriceSettingSerializer(serializers.Serializer):
    value = serializers.DecimalField(max_digits=19, decimal_places=2)  # noqa: WPS432, WPS110
