from rest_framework import serializers

from apps.helpers.serializers import EnumSerializer

from ..answer import TaskAnswerSerializer
from ..company import CompanySerializer
from ..ext import help_text
from ..file import FileArketaExtendedSerializer
from ..order_frequency_types import OrderFrequencyTypes
from ..question import QuestionArketaSerializer
from ..sku import SKUReadSerializer
from ..trade_point import TradePointArketaWithoutRegionReadSerializer
from .task_feedback import TaskArketaFeedbackCompactSerializer, TaskArketaFeedbackSerializer


class TaskArketaMobileSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=False)
    price = serializers.IntegerField(required=False)
    name = serializers.CharField()
    status = EnumSerializer(required=False)
    trade_point = TradePointArketaWithoutRegionReadSerializer()
    mobile_status = EnumSerializer(required=False)
    company = CompanySerializer()
    need_execution = serializers.BooleanField(required=False)
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    completion_date = serializers.DateField()
    days = serializers.ListField(child=serializers.DateField())
    frequency = serializers.ChoiceField(choices=OrderFrequencyTypes.choices)
    feedback_compact = TaskArketaFeedbackCompactSerializer(required=False)
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
    is_collection = serializers.BooleanField(required=False)
    collection_price = serializers.IntegerField(required=False)
    time = serializers.IntegerField()
    description = serializers.CharField()
    skues = SKUReadSerializer(many=True, required=False)
    questions = QuestionArketaSerializer(many=True)
    answers = TaskAnswerSerializer(many=True)
    show_type = serializers.CharField(required=False)
    type = EnumSerializer()
    question_on_first_screen = serializers.BooleanField()
    category = serializers.CharField(required=False)
    order = serializers.IntegerField(required=False)
    structure = serializers.ListField(child=serializers.CharField(), required=False, help_text=help_text)
    comment = serializers.CharField()
    additional_files = FileArketaExtendedSerializer(many=True)
    planogram = FileArketaExtendedSerializer()
    planograms = FileArketaExtendedSerializer(many=True)
    display_by_sku = serializers.BooleanField(required=False)
    feedback = TaskArketaFeedbackSerializer(required=False)
    withdraw_status = EnumSerializer(required=False)
    withdraw_error = serializers.CharField(required=False)
    is_onboarding_task = serializers.BooleanField(required=False)


class TaskArketaMobileCompactSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=False)
    name = serializers.CharField()
    trade_point = TradePointArketaWithoutRegionReadSerializer()
    company = CompanySerializer()


class TaskArketaTakeSerializer(serializers.Serializer):
    tasks = serializers.ListField(child=serializers.UUIDField())
    collection = serializers.UUIDField(required=False)
