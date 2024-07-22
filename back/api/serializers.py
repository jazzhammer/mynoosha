import math

from rest_framework import serializers

from .models import Client, WorkInterval
from django.utils import timezone
import pytz
# 2024-07-22 01:36:29.808000
timezone.activate(pytz.timezone('UTC'))


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            'name'
        ]


class WorkIntervalSerializer(serializers.ModelSerializer):
    hhmm = serializers.SerializerMethodField('get_hhmm')
    class Meta:
        model = WorkInterval
        fields = [
            'start',
            'stop',
            'start_utcms',
            'stop_utcms',
            'description',
            'client',
            'hhmm'
        ]

    def get_hhmm(self, instance):
        print(f"composing hhmm")
        if instance['stop_utcms']:
            stop = instance['stop_utcms']
            start = instance['start_utcms']
            diff = stop - start # seconds
            if diff < 3600:
                HH = 0
            else:
                HH = math.floor(diff / 3600)
            MM = math.floor((diff % 3600) / 60)
            hhstr = f'{HH}' if HH > 9 else f'0{HH}'
            mmstr = f'{MM}' if MM > 9 else f'0{MM}'
            hhmm = f'{hhstr}:{mmstr}'
            print(f"composed {hhmm}")
            return hhmm
        else:
            print(f"unable to compose with missing stop_utcms")
            return ''
