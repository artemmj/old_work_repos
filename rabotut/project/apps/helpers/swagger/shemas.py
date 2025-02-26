from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.utils import no_body

from .ext import BlankMeta, ReadOnly, WriteOnly


class TagsSwaggerAutoSchema(SwaggerAutoSchema):
    """
    Позволяет определять пользовательские теги для swagger схемы.

    see https://github.com/axnsan12/drf-yasg/issues/489
    Examples:
        class PageView(ApiView):
            ...
            swagger_tags = ['tag1']
            ...

        class PageView2(ApiView):
            ...
            swagger_tags = ['tag1 tag2']
            ...

        class PageView3(ApiView):
            ...
            swagger_tags = ['tag3']
            ...
    """

    def get_tags(self, operation_keys=None):
        operation_keys = operation_keys or self.operation_keys

        tags = self.overrides.get('tags')
        if not tags:
            tags = [operation_keys[0]]

        if hasattr(self.view, "swagger_tags"):
            tags = self.view.swagger_tags

        return tags


class ReadWriteAutoSchema(SwaggerAutoSchema):
    """Правильно генерирует спецификацию для read write полей.

    see https://github.com/axnsan12/drf-yasg/issues/70
    """

    def get_view_serializer(self):
        return self._convert_serializer(WriteOnly)

    def get_default_response_serializer(self):
        body_override = self._get_request_body_override()
        if body_override and body_override is not no_body:
            return body_override

        return self._convert_serializer(ReadOnly)

    def _convert_serializer(self, new_class):
        serializer = super().get_view_serializer()
        if not serializer:
            return serializer

        class CustomSerializer(new_class, serializer.__class__):
            class Meta(getattr(serializer.__class__, 'Meta', BlankMeta)):
                ref_name = new_class.__name__ + serializer.__class__.__name__

        new_serializer = CustomSerializer(data=serializer.data)
        return new_serializer


class CustomSwaggerAutoSchema(TagsSwaggerAutoSchema, ReadWriteAutoSchema):
    """Общая схема для генерации доки с поддержкой тегов и read write полей."""
