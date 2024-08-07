from django.db import models
from rest_framework import serializers

from ..model.worker import Worker
from ..model.client import Client


'''
ie. between a client and a worker, 
allows for attribution of a billable_type to a client so, among other things, a rate may be charged for work_intervals
'''
class Agreement(models.Model):
    name = models.CharField(max_length=128)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    worker = models.ForeignKey(Worker, on_delete=models.PROTECT)
    type = models.CharField(max_length=24)

class ClientWorker(models.Model):
    name = models.CharField(max_length=128)
    workers = models.ManyToManyField(Worker)

class AgreementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agreement
        fields = [
            'name',
            'client',
            'worker'
        ]