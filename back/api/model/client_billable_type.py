from rest_framework import serializers
from django.db import models

from ..model.client import Client
from ..model.billable_type import BillableType

""" 
we assign a billable type to a client any time a worker would want to attribute work_intervals to the client, of that type of work. 

eg. worker wants to attribute work_intervals for billable_type='landscaping' to client='jameson golf course'
a billable_type maybe assigned to a client multiple times, each with a different or the same rate. 
why would we do this ? because of agreements. 
the agreement of a client_billable_type makes the assignment unique, as an agreement could dictate the terms of a client_billable_type, 
likely captured elsewhere, eg, in a signed document. contracts in a series, year after year, could specify the same rates. 
"""
class ClientBillableType(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    billable_type = models.ForeignKey(BillableType, on_delete=models.PROTECT)
    amount = models.IntegerField()


class ClientBillableTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientBillableType
        fields = [
            'client',
            'billable_type',
            'amount',
        ]


