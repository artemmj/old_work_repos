from django.utils.deprecation import MiddlewareMixin

from apps.organization.models import Organization


class OrganizationMiddleware(MiddlewareMixin):
    organization_id_header = 'HTTP_ORGANIZATION_ID'

    def process_request(self, request):
        request.organization = None
        organization_id = request.META.get(self.organization_id_header, None)

        if organization_id:
            request.organization = Organization.objects.filter(id=organization_id).first()
