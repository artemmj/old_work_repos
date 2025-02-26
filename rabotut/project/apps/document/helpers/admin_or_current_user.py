from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.user.models import UserRoles

User = get_user_model()


class AdminOrCurrentUserDefault(serializers.CurrentUserDefault):
    def __call__(self, serializer_field):
        context = serializer_field.context
        user = context['request'].user
        if user.role != UserRoles.MASTER:
            # Если запрашивает не админ, значит документ загружает пользователь, вернуть его
            return context['request'].user
        # Иначе грузит админ, требуется поле user, в котором передать айди юзера к которому привязываем документ
        if 'user' not in context['request'].data:
            raise ValidationError('Требуется поле user при загрузке документа админом.')
        return get_object_or_404(User, id=context['request'].data['user'])
