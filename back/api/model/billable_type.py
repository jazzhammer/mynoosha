from rest_framework import serializers
from django.db import models

"""
a name, among other fields, that distinguishes one type of activity from another, which a worker would want to attribute a work_interval.
eg. billable_type == 'landscaping' or 'designing'

we intersect a billable_type with a client as a client_billable_type to indicate a rate to be charged to the client
see client_billable_type
"""
class BillableType(models.Model):
    name = models.CharField(max_length=32)


class BillableTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillableType
        fields = [
            'name'
        ]

