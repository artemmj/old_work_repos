from rest_framework import serializers

from api.v1.employee.serializers import EmployeeShortReadSerializer
from apps.event.models import Event, TitleChoices
from apps.terminal.models import Terminal


class TerminalWriteSerializer(serializers.ModelSerializer):
    mac_address = serializers.CharField(required=True)
    device_model = serializers.CharField(required=True)

    class Meta:
        model = Terminal
        fields = ('id', 'project', 'ip_address', 'number', 'mac_address', 'device_model')
        read_only_fields = ('id',)

    def create(self, validated_data):
        project = validated_data['project']
        mac_address = validated_data.get('mac_address')
        exist_terminal_in_project = Terminal.objects.filter(project=project).filter(mac_address=mac_address)
        if exist_terminal_in_project:
            return exist_terminal_in_project[0]
        exist_terminals = Terminal.objects.filter(mac_address=mac_address)
        if exist_terminals:
            data = exist_terminals[0]
            validated_data['number'] = data.number
            validated_data['mac_address'] = data.mac_address
            validated_data['device_model'] = data.device_model
        comment = (
            f'Запущен процесс загрузки терминала в проекте '
            f'{validated_data["project"]} с номером: {validated_data["number"]}'  # noqa: WPS326
        )
        Event.objects.create(project=project, title=TitleChoices.TERMINAL_LOAD_START, comment=comment)
        return super().create(validated_data)


class TerminalReadSerializer(serializers.ModelSerializer):
    employee = EmployeeShortReadSerializer()

    class Meta:
        model = Terminal
        fields = ('id', 'number', 'ip_address', 'db_loading', 'last_connect', 'employee', 'mac_address')
        read_only_fields = ('id',)


class TerminalConnectSerializer(serializers.Serializer):
    employee_number = serializers.IntegerField(required=True)
    terminal = serializers.PrimaryKeyRelatedField(queryset=Terminal.objects.all(), required=True)


class TerminalUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terminal
        fields = ('number',)
