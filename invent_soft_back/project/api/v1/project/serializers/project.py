from rest_framework import serializers

from api.v1.project.serializers._project_stats_service import ProjectStatisticService  # noqa: WPS436
from api.v1.user.serializers import UserReadSerializer
from apps.changelog.models import ChangeLog, ChangeLogActionType, ChangeLogModelType
from apps.event.models import Event, TitleChoices
from apps.file.models import File
from apps.helpers.serializers import EagerLoadingSerializerMixin
from apps.project.models import Project
from apps.template.models import Template, TemplateExport


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'created_at', 'title', 'address')
        read_only_fields = ('id', 'created_at')


class ProjectRetrieveSerializer(EagerLoadingSerializerMixin, serializers.ModelSerializer):
    manager = UserReadSerializer()
    statistic = serializers.SerializerMethodField()

    select_related_fields = ('manager',)

    class Meta:
        model = Project
        fields = (
            'id',
            'created_at',
            'title',
            'address',
            'manager',
            'rmm_settings',
            'terminal_settings',
            'template',
            'template_export',
            'auto_assign_enbale',
            'accounting_without_yk',
            'statistic',
        )

    def get_statistic(self, instance):
        return ProjectStatisticService(instance=instance).process()


class ProjectWriteSerializer(serializers.ModelSerializer):
    manager = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Project
        fields = (
            'id',
            'created_at',
            'title',
            'address',
            'manager',
            'template',
            'template_export',
            'accounting_without_yk',
            'auto_assign_enbale',
        )
        read_only_fields = ('id', 'created_at')

    def create(self, validated_data):
        instance = super().create(validated_data)
        Event.objects.create(
            title=TitleChoices.CREATE_NEW_PROJECT,
            comment=f'Создан новый проект {validated_data["title"]}.',
            project=instance,
        )
        return instance

    def update(self, instance, validated_data):
        dict_val_data = validated_data.copy()

        if 'manager' in dict_val_data:
            dict_val_data['manager'] = str(dict_val_data['manager'].pk)
        if 'template' in dict_val_data:
            dict_val_data['template'] = str(dict_val_data['template'].pk)
        if 'template_export' in dict_val_data:
            dict_val_data['template_export'] = str(dict_val_data['template_export'].pk)

        instance = super().update(instance, validated_data)

        ChangeLog.objects.create(
            project=instance,
            model=ChangeLogModelType.PROJECT,
            record_id=instance.pk,
            action_on_model=ChangeLogActionType.UPDATE,
            changed_data=dict_val_data,
        )
        Event.objects.create(
            title=TitleChoices.PROJECT_SETTINGS_UPDATE,
            comment=self._create_text_for_event(validated_data, instance),
            project=instance,
        )
        return instance

    def _create_text_for_event(self, validated_data: dict, instance: Project):
        comment = f'Изменены настройки проекта {instance.title}, новые параметры:\n\n'
        for key, value in validated_data.items():
            _key = getattr(Project, key).field.verbose_name  # noqa: WPS122
            comment += f'{_key} == {value}\r\n'
        return comment


class CheckPasswordProjectRequestSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, max_length=10)


class CheckPasswordProjectResponseSerializer(serializers.Serializer):
    result = serializers.BooleanField(required=True)


class ImportProjectSettingsSerializer(serializers.Serializer):
    file = serializers.PrimaryKeyRelatedField(queryset=File.objects.all())
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    def to_representation(self, instance):
        return {
            'file': instance['file'].id,
            'project': instance['project'].id,
        }


class ImportProductSerializer(serializers.Serializer):
    file = serializers.PrimaryKeyRelatedField(queryset=File.objects.all())
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    template = serializers.PrimaryKeyRelatedField(queryset=Template.objects.all())

    def to_representation(self, instance):
        return {
            'file': instance['file'].id,
            'project': instance['project'].id,
            'template': instance['template'].id,
        }


class DeleteProductSerializer(serializers.Serializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    params = serializers.MultipleChoiceField(
        choices={
            ('delete_all', 'Удалить товары'),
            ('delete_remainders', 'Удалить остатки'),
            ('delete_prices', 'Удалить цены'),
        },
        required=False,
    )

    def to_representation(self, instance):
        return {
            'project': instance.get('project').id,
            'params': list(instance.get('params')) if instance.get('params') else [],
        }


class ExportDocumentSerializer(serializers.Serializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    template = serializers.PrimaryKeyRelatedField(queryset=TemplateExport.objects.all())
    format = serializers.ChoiceField(
        choices=(
            ('csv', '.CSV'),
            ('txt', '.TXT'),
        ),
        required=True,
    )

    def to_representation(self, instance):
        return {
            'project': instance['project'].id,
            'template': instance['template'].id,
            'format': instance['format'],
        }


class ImportProjectSerializer(serializers.Serializer):
    file = serializers.PrimaryKeyRelatedField(queryset=File.objects.all())

    def to_representation(self, instance):
        return {
            'file': instance['file'].id,
        }
