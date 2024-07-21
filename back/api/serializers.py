from rest_framework import serializers

from .models import Client, WorkInterval
from django.utils import timezone
import pytz
timezone.activate(pytz.timezone('UTC'))

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            'name'
        ]

class WorkIntervalSerializer(serializers.ModelSerializer):
    # start_utcms = serializers.SerializerMethodField()
    # stop_utcms = serializers.SerializerMethodField()
    class Meta:
        model = WorkInterval
        fields = [
            'start',
            'stop',
            'start_utcms',
            'stop_utcms',
            'description',
            'client',
        ]

    # def get_start_utcms(self, instance):
    #     start_utcms = round(instance.start.timestamp())
    #     print(f'calculated {start_utcms}')
    #     return start_utcms
    #
    # def get_stop_utcms(self, instance):
    #     stop_utcms = round(instance.start.timestamp())
    #     print(f'calculated {stop_utcms}')
    #     return stop_utcms
