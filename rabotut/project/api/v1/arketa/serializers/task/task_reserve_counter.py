from rest_framework import serializers


class TaskArketaReserveCounterSerializer(serializers.Serializer):
    available = serializers.IntegerField(help_text='Кол-во задач, доступных к бронированию пользователем.')
    max = serializers.IntegerField(help_text='Максимальное кол-во задач, которое может забронировать пользователь')
