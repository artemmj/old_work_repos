from constance import config
from django.contrib.auth import get_user_model
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404
from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import decorators, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

import settings
from api.v1.user import (  # noqa: WPS235
    ConfirmCodeSerializer,
    PasswordResetByCodeSerializer,
    SendCodeRegistrationSerializer,
    SendCodeSerializer,
    UserAdminCompactSerializer,
    UserChangePasswordSerializer,
    UserCompactSerializer,
    UserCreateSerializer,
    UserReadSerializer,
    UserRegistrationSerializer,
    filters,
    serializers,
)
from apps.helpers import exceptions
from apps.helpers import permissions as permissions_helper
from apps.helpers import serializers as serializers_helper
from apps.helpers.celery import CeleryResultSerializer, CeleryTaskWrapper
from apps.helpers.permissions import IsAdministrator, IsCustomer, IsDispatcher, IsInspector, IsSuperUser
from apps.helpers.viewsets import paginate_response
from apps.user.managers import UserManager
from apps.user.models import RoleChoices
from apps.user.tasks import users_export_excel

from .auth import AuthViewSet

User = get_user_model()


class UserViewSet(AuthViewSet):  # noqa: WPS214
    serializer_class = serializers.UserWriteSerializer
    serializer_class_map = {
        **AuthViewSet.serializer_class_map,
        'list': UserReadSerializer,
        'retrieve': UserReadSerializer,
        'create': UserCreateSerializer,
        'me': UserReadSerializer,
        'registration': UserRegistrationSerializer,
        'compact': UserCompactSerializer,
        'password_reset_by_code': PasswordResetByCodeSerializer,
        'change_password': UserChangePasswordSerializer,
        'confirm_code': ConfirmCodeSerializer,
        'send_code_registration': SendCodeRegistrationSerializer,
        'send_code': SendCodeSerializer,
        'admin_compact': UserAdminCompactSerializer,
        'admin_change_password': UserChangePasswordSerializer,
    }
    permission_classes = (permissions.IsAuthenticated,)
    permission_map = {
        **AuthViewSet.permission_map,
        'create': (IsSuperUser | IsDispatcher | IsAdministrator),
        'update': (IsInspector | IsSuperUser | IsDispatcher | IsAdministrator | IsCustomer),
        'partial_update': (IsInspector | IsSuperUser | IsDispatcher | IsAdministrator | IsCustomer),
        'registration': permissions.AllowAny,
        'confirm_code': permissions.AllowAny,
        'destroy': (permissions_helper.IsSuperUser | IsDispatcher | IsAdministrator),
        'password_reset_by_code': permissions.AllowAny,
        'send_code_registration': permissions.AllowAny,
        'send_code': permissions.AllowAny,
        'admin_compact': (IsSuperUser | IsDispatcher | IsAdministrator),
        'admin_deactivate_inspector': (IsSuperUser | IsDispatcher | IsAdministrator),
        'admin_activate_inspector': (IsSuperUser | IsDispatcher | IsAdministrator),
        'admin_export_excel': (IsSuperUser | IsDispatcher | IsAdministrator),
        'admin_change_password': (IsSuperUser | IsDispatcher | IsAdministrator),
    }

    search_fields = ('first_name', 'middle_name', 'last_name', 'phone')
    ordering_fields = ('first_name', 'middle_name', 'last_name', 'phone', 'is_inspector')
    filterset_class = filters.UserFilterSet

    default_responses = {
        400: exceptions.BadRequestResponseSerializer,
        410: exceptions.BadRequestResponseSerializer,
    }

    def get_queryset(self):  # noqa: WPS615
        user = self.request.user
        queryset = UserManager().get_queryset(user)
        if not user.is_authenticated:
            return queryset.none()

        return queryset.exclude(phone=settings.REMOTE_USER_PHONE)

    @swagger_auto_schema(
        request_body=UserCreateSerializer,
        responses={201: UserReadSerializer, 400: exceptions.BadRequestResponseSerializer},
    )
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserReadSerializer(user).data, status=status.HTTP_201_CREATED)

    @decorators.action(methods=['get'], detail=False)
    def me(self, request, **kwargs):
        """Получение своих данных."""
        serializer = self.get_serializer(instance=request.user)
        return Response(serializer.data)

    @decorators.action(methods=['get'], detail=False)
    def compact(self, request):
        """Список пользователей с урезанными данными."""
        return super().list(request)  # noqa: WPS613

    @swagger_auto_schema(
        request_body=UserRegistrationSerializer,
        responses={201: UserReadSerializer, 400: exceptions.BadRequestResponseSerializer},
    )
    @decorators.action(methods=['post'], detail=False)
    def registration(self, request):
        """Регистрация."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)   # noqa:  WPS204
        user = serializer.save()
        data = serializers.UserReadSerializer(instance=user, context=self.get_serializer_context()).data  # noqa: WPS110
        return Response(data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=ConfirmCodeSerializer,
        responses={200: serializers_helper.EmptySerializer, 400: exceptions.BadRequestResponseSerializer},
    )
    @decorators.action(methods=['post'], detail=False)
    def confirm_code(self, request, *args, **kwargs):
        """Подтверждение кода."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=PasswordResetByCodeSerializer,
        responses={200: serializers_helper.EmptySerializer, 400: exceptions.BadRequestResponseSerializer},
    )
    @decorators.action(methods=['post'], detail=False)
    def password_reset_by_code(self, request):
        """Изменить пароль по коду."""
        user = get_object_or_404(User, phone=request.data['phone'])
        serializer = self.get_serializer(data=request.data, instance=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: UserChangePasswordSerializer, 400: exceptions.BadRequestResponseSerializer})
    @decorators.action(methods=['post'], detail=False, url_path='change-password')
    def change_password(self, request):
        """Изменить пароль."""
        serializer = self.get_serializer(data=request.data, instance=request.user)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = serializers.UserReadSerializer(instance=user).data  # noqa: WPS110
        return Response(data)

    @swagger_auto_schema(
        request_body=SendCodeSerializer,
        responses={200: serializers_helper.EmptySerializer, 400: exceptions.BadRequestResponseSerializer},
    )
    @decorators.action(methods=['post'], detail=False)
    def send_code(self, request):
        """Отправка кода подтверждения на телефон пользователя."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(request.data)
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=SendCodeRegistrationSerializer,
        responses={200: serializers_helper.EmptySerializer, 409: exceptions.BadRequestResponseSerializer},
    )
    @decorators.action(methods=['post'], detail=False)
    def send_code_registration(self, request):
        """Отправка кода подтверждения на телефон пользователя при регистрации."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(request.data)
        return Response(status=status.HTTP_200_OK)

    @decorators.action(methods=['get'], detail=False, url_path='admin/compact')
    def admin_compact(self, request):
        """Список пользователей с урезанными данными для админки."""
        qs = self.get_queryset()
        qp = self.request.query_params
        if 'ordering' in qp and 'is_inspector' in qp['ordering']:
            if qp['ordering'] == '-is_inspector':
                qs = qs.order_by('-roles')
            elif qp['ordering'] == 'is_inspector':
                qs = qs.order_by('roles')
        else:
            qs = self.filter_queryset(self.get_queryset())
        return paginate_response(self, qs, UserAdminCompactSerializer)

    @swagger_auto_schema(request_body=no_body, responses={
        status.HTTP_200_OK: UserReadSerializer,
        status.HTTP_400_BAD_REQUEST: exceptions.BadRequestResponseSerializer,
    })
    @decorators.action(methods=['post'], detail=True, url_path='admin/deactivate_inspector')
    def admin_deactivate_inspector(self, request, pk=None):
        """Убрать роль инспектора у пользователя."""
        instance = self.get_object()
        if not instance.inspectors.exists():  # noqa: DAR401
            raise ValidationError({'error': config.USER_HAVE_NOT_INSPECTOR_INFO_ERROR})
        if RoleChoices.INSPECTOR in instance.roles:
            instance.roles.remove(RoleChoices.INSPECTOR)
            instance.save()
        return Response(UserReadSerializer(instance=instance).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=no_body, responses={
        status.HTTP_200_OK: UserReadSerializer,
        status.HTTP_400_BAD_REQUEST: exceptions.BadRequestResponseSerializer,
    })
    @decorators.action(methods=['post'], detail=True, url_path='admin/activate_inspector')
    def admin_activate_inspector(self, request, pk=None):
        """Добавить роль инспектора пользователю."""
        instance = self.get_object()
        if not instance.inspectors.exists():  # noqa: DAR401
            raise ValidationError({'error': config.USER_HAVE_NOT_INSPECTOR_INFO_ERROR})
        if RoleChoices.INSPECTOR not in instance.roles:
            instance.roles.append(RoleChoices.INSPECTOR)
            instance.save()
        return Response(UserReadSerializer(instance=instance).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=no_body, responses={
        status.HTTP_200_OK: CeleryResultSerializer,
        status.HTTP_400_BAD_REQUEST: exceptions.BadRequestResponseSerializer,
    })
    @decorators.action(methods=['post'], detail=False, filterset_class=None, url_path='admin/export_excel')
    def admin_export_excel(self, request):
        """Выгрузить пользователей в excel файл."""
        host = f'{request.scheme}://{request.get_host()}'
        task = users_export_excel.delay(host)
        return Response({'result_id': task.id}, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={
        200: UserChangePasswordSerializer,
        400: exceptions.BadRequestResponseSerializer,
    })
    @decorators.action(methods=['post'], detail=True, url_path='admin/change_password')
    def admin_change_password(self, request, pk=None):
        """Изменить пароль пользователя из админки."""
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = serializers.UserReadSerializer(instance=user).data  # noqa: WPS110
        return Response(data)
