from rest_framework import serializers

from .models import Client, WorkInterval


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            'name'
        ]

class WorkIntervalSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkInterval
        fields = [
            'start',
            'stop',
            'description',
            'client',
        ]