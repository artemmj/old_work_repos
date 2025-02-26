from rest_framework.permissions import IsAuthenticated

from apps.helpers.viewsets import ListExtendedModelViewSet
from apps.projects.models import Project

from .serializers import ProjectSerializer


class ProjectViewSet(ListExtendedModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated,)
    search_fields = ('name',)
