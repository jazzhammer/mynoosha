from rest_framework import serializers
from django.db import models

from api.model import Worker, Agreement


class WorkerRate(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.PROTECT)
    agreement = models.ForeignKey(Agreement, on_delete=models.PROTECT)
    amount_rate = models.IntegerField(default=0)

class WorkerRateSerializer(serializers.ModelSerializer):
    class Meta:

        model = WorkerRate
        fields = [
            'worker',
            'amount_rate',
            'agreement'
        ]


