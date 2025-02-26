from rest_framework import serializers

from apps.helpers.serializers import EnumSerializer


class QuestionReasonSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()


class ShelfCameraSettings(serializers.Serializer):
    max_size = serializers.IntegerField()
    compression = serializers.FloatField(min_value=0, max_value=1)
    angle = serializers.FloatField(min_value=0)
    crop = serializers.BooleanField()
    aspect_ratio = serializers.CharField()
    width = serializers.IntegerField(min_value=100)
    height = serializers.IntegerField(min_value=100)
    grid = serializers.BooleanField()
    zoom = serializers.BooleanField()
    on_click_focus = serializers.BooleanField()
    flash = serializers.BooleanField()
    max_rows = serializers.IntegerField(min_value=1)
    phantom_height = serializers.FloatField(min_value=0)
    phantom_width = serializers.FloatField(min_value=0)
    phantom_transparency = serializers.FloatField(min_value=0)


class RecognitionCameraSettings(serializers.Serializer):
    main = ShelfCameraSettings()
    open_fridge = ShelfCameraSettings()
    closed_fridge = ShelfCameraSettings()
    shelf = ShelfCameraSettings()
    checkout_zone = ShelfCameraSettings()
    promo = ShelfCameraSettings()
    refrigerator = ShelfCameraSettings()


class QuestionArketaSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=False)
    name = serializers.CharField()
    is_required = serializers.BooleanField(required=False)
    is_conditional = serializers.BooleanField(required=False)
    required = serializers.BooleanField(required=False)
    order = serializers.IntegerField(required=False)
    type = serializers.CharField()
    choices = serializers.ListField(child=serializers.CharField(), required=False)
    reasons = QuestionReasonSerializer(many=True, required=False)
    shelf_types = EnumSerializer(many=True, required=False)
    recognition_camera_settings = RecognitionCameraSettings(required=False)
    photo_camera_settings = RecognitionCameraSettings(required=False)
    attachment_type = serializers.CharField(required=False)
    is_take_photo_all_goods = serializers.BooleanField(required=False)
    is_entry_prices = serializers.BooleanField(required=False)
    is_required_absence_reason = serializers.BooleanField(required=False)
    is_required_photo_confirm = serializers.BooleanField(required=False)
