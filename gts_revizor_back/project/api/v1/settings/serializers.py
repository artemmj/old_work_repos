from rest_framework import serializers


class SettingsSerializer(serializers.Serializer):
    key = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()  # noqa: WPS110

    def get_key(self, settings):
        return settings[0]

    def get_value(self, settings):
        return settings[1]


class BuildVersionSerializer(serializers.Serializer):
    build_version = serializers.CharField()
