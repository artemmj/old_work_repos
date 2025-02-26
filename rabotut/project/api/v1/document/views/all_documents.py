from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.document.serializers.all_documents import AllDocumentsSerializer, QueryAllDocumentsSerializer
from apps.document.services import DocumentsOfUserService
from apps.helpers.exceptions import ErrorResponseSerializer
from apps.user.models import User
from apps.user.permissions import IsApplicantPermission, IsMasterPermission


class DocumentViewSet(viewsets.GenericViewSet):
    serializer_class = AllDocumentsSerializer
    permission_classes = (IsMasterPermission | IsApplicantPermission,)
    permission_map = {
        'all': IsMasterPermission,
    }

    @swagger_auto_schema(
        query_serializer=QueryAllDocumentsSerializer(),
        operation_summary='Получение всех документов и их статуса',
        responses={
            status.HTTP_200_OK: AllDocumentsSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
            status.HTTP_404_NOT_FOUND: ErrorResponseSerializer(many=True),
        },
    )
    @action(detail=False, methods=['GET'])
    def all(self, request):
        query_serializer = QueryAllDocumentsSerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        user_phone = query_serializer.validated_data.get('user_phone')
        user = request.user
        if IsMasterPermission().has_permission(request, self) and user_phone:
            user = get_object_or_404(User, phone=user_phone)
        user_documents = DocumentsOfUserService().process(user=user if user else request.user)
        serializer = self.get_serializer(user_documents)
        return Response(serializer.data, status=status.HTTP_200_OK)
