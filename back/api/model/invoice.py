from rest_framework import serializers
from django.db import models

from ..model.client import Client


class Invoice(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    issued = models.DateTimeField(editable=True, null=True)
    created = models.DateTimeField(auto_now=True)


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = [
            'client'
        ]
