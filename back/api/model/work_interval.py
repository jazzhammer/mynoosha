import math
from django.utils import timezone
import pytz
timezone.activate(pytz.timezone('UTC'))

from rest_framework import serializers
from django.db import models

from .worker import Worker
from .invoice_item import InvoiceItem
from .client import Client


class WorkInterval(models.Model):
    # id = modelObjectIdField(db_column="_id", primary_key=True)
    start = models.DateTimeField()
    stop = models.DateTimeField(null=True)
    start_utcms = models.BigIntegerField(null=True)
    stop_utcms = models.BigIntegerField(null=True)
    description = models.TextField(null=True, blank=True)
    client = models.ForeignKey(Client, null=False, on_delete=models.PROTECT)
    invoice_item = models.ForeignKey(InvoiceItem, null=True, on_delete=models.PROTECT)
    worker = models.ForeignKey(Worker, null=True, on_delete=models.PROTECT)

    class Meta:
        indexes = [models.Index(fields=['start_utcms'])]

    def save(self, *args, **kwargs):
        if isinstance(self.start, str):
            if self.start.endswith('Z'):
                self.start = self.start[:-1]
            utc = timezone.datetime.fromisoformat(self.start)
        else:
            utc = self.start
        self.start_utcms = round(utc.timestamp())
        if self.stop:
            if isinstance(self.stop, str):
                if self.stop.endswith('Z'):
                    self.stop = self.stop[:-1]
                utc = timezone.datetime.fromisoformat(self.stop)
            else:
                utc = self.stop
            self.stop_utcms = round(utc.timestamp())
        super(WorkInterval, self).save(*args, **kwargs)

class WorkIntervalSerializer(serializers.ModelSerializer):
    hhmm = serializers.SerializerMethodField('get_hhmm')

    class Meta:
        model = WorkInterval
        fields = (
            'pk',
            'id',
            'start',
            'stop',
            'start_utcms',
            'stop_utcms',
            'description',
            'client',
            'worker',
            'hhmm',
            'invoice_item',
        )

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
