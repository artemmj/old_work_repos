from rest_framework.permissions import IsAuthenticated

from apps.departments.models import Department
from apps.helpers.viewsets import ListExtendedModelViewSet

from .serializers import DepartmentSerializer


class DepartmentViewSet(ListExtendedModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = (IsAuthenticated,)
    search_fields = ('name',)
