from drf_yasg import openapi

organization_id_header = openapi.Parameter(
    'organization-id',
    openapi.IN_HEADER,
    description='ID организации',
    type=openapi.IN_HEADER,
    required=False,
)
