from apps.helpers.services import AbstractService


class TemplateSettingsUpdateService(AbstractService):
    """Сервис обновления настроек шаблона."""

    def process(self, instance, validated_data, context, serializer_class=None):
        detail_data = validated_data.pop('detail', '')
        if detail_data and serializer_class:
            detail = instance.detail
            serializer = serializer_class(instance=detail, data=detail_data, partial=True, context=context)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
