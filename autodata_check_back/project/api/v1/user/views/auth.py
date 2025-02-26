from django.conf import settings
from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist
from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import authentication, decorators, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt import authentication as authentication_jwt
from rest_framework_simplejwt import serializers as jwt_serializers
from rest_framework_simplejwt import views

from api.v1.user import CustomTokenObtainPairSerializer, serializers
from apps.helpers import batchmixin, exceptions, viewsets
from apps.helpers.custom_error import CustomValidationError
from apps.user.managers import UserManager
from apps.user.models import User


class AuthViewSet(views.TokenViewBase, viewsets.CRUDExtendedModelViewSet, batchmixin.DeleteBatchMixin):  # noqa: WPS214
    serializer_class = serializers.UserUpdateSerializer
    serializer_class_map = {
        'login': CustomTokenObtainPairSerializer,
        'refresh': jwt_serializers.TokenRefreshSerializer,
    }
    permission_classes = (permissions.IsAuthenticated,)
    permission_map = {
        'login': permissions.AllowAny,
        'refresh': permissions.AllowAny,
    }
    authentication_classes = (authentication_jwt.JWTAuthentication, authentication.SessionAuthentication)

    default_responses = {
        400: exceptions.BadRequestResponseSerializer,
        404: exceptions.BadRequestResponseSerializer,
        403: exceptions.BadRequestResponseSerializer,
        410: exceptions.BadRequestResponseSerializer,
    }

    def get_queryset(self):  # noqa: WPS615
        user = self.request.user
        queryset = UserManager().get_queryset(user)
        if not user.is_authenticated:
            return queryset.none()

        return queryset.exclude(phone=settings.REMOTE_USER_PHONE)

    @swagger_auto_schema(
        request_body=serializers.LoginSerializer,
        responses={status.HTTP_200_OK: CustomTokenObtainPairSerializer()},
    )
    @decorators.action(methods=['post'], detail=False)
    def login(self, request):
        if not User.objects.filter(phone=request.data['phone']).exists():
            raise CustomValidationError(
                {'detail': 'Не найдено', 'code': 'not_found'},
                status_code=status.HTTP_404_NOT_FOUND,
            )
        serializer = serializers.LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return super().post(request)  # noqa: WPS613

    @swagger_auto_schema(responses={status.HTTP_200_OK: jwt_serializers.TokenObtainPairSerializer()})
    @decorators.action(methods=['post'], detail=False)
    def refresh(self, request):
        return super().post(request)  # noqa: WPS613

    @swagger_auto_schema(request_body=no_body, responses={status.HTTP_200_OK: 'No content'})
    @decorators.action(methods=['post'], detail=False)
    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass   # noqa: WPS420

        logout(request)
        return Response(status=status.HTTP_200_OK)
