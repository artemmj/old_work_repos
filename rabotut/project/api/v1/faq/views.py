from rest_framework.permissions import AllowAny

from apps.faq.models import Faq
from apps.helpers.viewsets import ListExtendedModelViewSet

from .serializers import FaqSerializer


class FaqViewSet(ListExtendedModelViewSet):
    queryset = Faq.objects.all()
    serializer_class = FaqSerializer
    permission_classes = (AllowAny,)
