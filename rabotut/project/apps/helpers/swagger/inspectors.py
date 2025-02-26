from collections import OrderedDict

import coreapi
import coreschema
from drf_yasg import openapi
from drf_yasg.inspectors import FilterInspector
from drf_yasg.utils import force_real_str


class ArrayFilterInspector(FilterInspector):
    """Кастомный инспектор для генерации множественных query-параметров."""

    coreapi_types = {
        coreschema.Integer: openapi.TYPE_INTEGER,
        coreschema.Number: openapi.TYPE_NUMBER,
        coreschema.String: openapi.TYPE_STRING,
        coreschema.Boolean: openapi.TYPE_BOOLEAN,
        coreschema.Array: openapi.TYPE_ARRAY,
    }

    def get_filter_parameters(self, filter_backend):
        fields = []
        if hasattr(filter_backend, 'get_schema_fields'):
            fields = filter_backend.get_schema_fields(self.view)
        return [self.coreapi_field_to_parameter(field) for field in fields]

    def coreapi_field_to_parameter(self, field: coreapi.Field) -> openapi.Parameter:
        location_to_in = {
            'query': openapi.IN_QUERY,
            'path': openapi.IN_PATH,
            'form': openapi.IN_FORM,
            'body': openapi.IN_FORM,
        }
        coreschema_attrs = ['format', 'pattern', 'enum', 'min_length', 'max_length']
        schema = field.schema
        return openapi.Parameter(
            name=field.name,
            in_=location_to_in[field.location],
            required=field.required,
            description=force_real_str(schema.description) if schema else None,
            type=self.coreapi_types.get(type(schema), openapi.TYPE_STRING),
            items=self.make_items_schema(schema) if type(schema) is coreschema.Array else None,
            **OrderedDict((attr, getattr(schema, attr, None)) for attr in coreschema_attrs)
        )

    @classmethod
    def make_items_schema(cls, parent_field) -> openapi.Items:
        items_schema = parent_field.items

        coreschema_attrs = ['format', 'pattern', 'enum']
        return openapi.Items(
            type=cls.coreapi_types.get(type(items_schema), openapi.TYPE_STRING),
            **OrderedDict((attr, getattr(items_schema, attr, None)) for attr in coreschema_attrs),
        )
