import structlog
from constance import config
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.helpers.exceptions import ErrorResponseSerializer
from apps.helpers.sms.phone_secret import PhoneSecretService
from apps.helpers.sms.red_sms import RedSmsService
from apps.helpers.viewsets import RUDExtendedModelViewSet
from apps.user.services import CreateUserService

from . import serializers

User = get_user_model()
log = structlog.get_logger()


class MobileViewSet(RUDExtendedModelViewSet):
    swagger_tags = ['user']
    serializer_class_map = {
        'login': serializers.UserRequestLoginSerializer,
        'send_code': serializers.UserRequestCodeWriteSerializer,
    }
    permission_map = {
        'send_code': permissions.AllowAny,
        'login': permissions.AllowAny,
    }

    @swagger_auto_schema(
        request_body=serializers.UserRequestCodeWriteSerializer(),
        operation_summary='подтверждение номера телефона и получения кода для регистрации',
        responses={
            status.HTTP_200_OK: serializers.UserCodeResponseSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    @action(methods=['post'], detail=False, url_path='mobile/send_code')
    def send_code(self, request):
        """Получение кода для регистрации."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        CreateUserService().process(phone=phone)
        result_generate_code = PhoneSecretService().process(phone=phone)
        result_send_code = False
        if not config.SMS_CODE_IN_RESPONSE:
            result_send_code = RedSmsService(message=result_generate_code['message'], phone=phone).process()
        response_data = {
            'phone': result_generate_code['phone'],
            'code': result_generate_code['code'],
            'is_sent': result_send_code,
        }
        data = serializers.UserCodeResponseSerializer(instance=response_data).data  # noqa: WPS110
        return Response(data)

    @swagger_auto_schema(
        request_body=serializers.UserRequestLoginSerializer(),
        responses={
            status.HTTP_200_OK: serializers.UserRequestLoginSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ErrorResponseSerializer(many=True),
            status.HTTP_404_NOT_FOUND: ErrorResponseSerializer(many=True),
        },
    )
    @action(methods=['post'], detail=False, url_path='mobile/login')
    def login(self, request):
        """Получение access и refresh токена по коду авторизации."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        code = serializer.validated_data['code']
        user = User.objects.filter(phone=phone).first()
        if not user or not PhoneSecretService().is_valid_code(phone, code):
            log.warning('Неверный код или номер.')
            raise ValidationError('Неверный код или номер.')
        refresh = RefreshToken.for_user(user)
        PhoneSecretService().clear(phone)
        payload = {'access': str(refresh.access_token), 'refresh': str(refresh)}
        return Response(payload, status=status.HTTP_200_OK)
