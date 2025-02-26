from rest_framework import mixins, permissions

from api.v1.transaction.serializers.inspector import InspectorTransactionReadSerializer
from apps.helpers.permissions import IsAdministrator, IsDispatcher, IsInspector, IsSuperUser
from apps.helpers.viewsets import ExtendedGenericViewSet
from apps.transaction.models import InspectorTransaction


class InspectorTransactionViewSet(ExtendedGenericViewSet, mixins.ListModelMixin):
    queryset = InspectorTransaction.objects.all()
    serializer_class = InspectorTransactionReadSerializer
    permission_classes = (permissions.IsAuthenticated,)
    permission_map = {
        'list': (IsInspector | IsSuperUser | IsAdministrator | IsDispatcher),
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        if (IsSuperUser | IsAdministrator | IsDispatcher)().has_permission(self.request, self):
            return queryset
        if IsInspector().has_permission(self.request, self):
            return queryset.filter(inspector__user=self.request.user)
        return queryset.none()
