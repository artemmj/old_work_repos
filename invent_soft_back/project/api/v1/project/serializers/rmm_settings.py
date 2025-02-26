from rest_framework import serializers

from apps.changelog.models import ChangeLog, ChangeLogActionType, ChangeLogModelType
from apps.event.models import Event, TitleChoices
from apps.project.models import RMMSettings


class RMMSettingsUpdateSerializer(serializers.ModelSerializer):  # noqa: WPS338
    class Meta:
        model = RMMSettings
        fields = ('id', 'auto_zones_amount', 'password', 'norm', 'extended_tasks')
        read_only_fields = ('id',)

    def _create_text_for_event(self, validated_data: dict, instance: RMMSettings):
        comment = f'Изменены настройки РММ проекта {instance.project.title}, новые параметры:\n\n'
        for key, value in validated_data.items():
            _key = getattr(RMMSettings, key).field.verbose_name  # noqa: WPS122
            comment += f'{_key} == {value}\r\n'
        return comment

    def update(self, instance, validated_data):
        obj = super().update(instance, validated_data)

        if 'auto_zones_amount' in validated_data and validated_data['auto_zones_amount'] == 0:
            instance.project.auto_assign_enbale = False
            instance.project.save()

        ChangeLog.objects.create(
            project=obj.project,
            model=ChangeLogModelType.RMM_SETTINGS,
            record_id=instance.pk,
            action_on_model=ChangeLogActionType.UPDATE,
            changed_data=validated_data,
        )

        Event.objects.create(
            project=obj.project,
            title=TitleChoices.TERMINAL_SETTINGS_UPDATE,
            comment=self._create_text_for_event(validated_data, instance),
        )
        return obj


class RMMSettingsReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = RMMSettings
        fields = ('id', 'auto_zones_amount', 'password', 'norm', 'extended_tasks')
        read_only_fields = ('id',)
