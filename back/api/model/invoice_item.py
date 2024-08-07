from rest_framework import serializers
from django.db import models

from .invoice import Invoice
from ..model.client import Client
from ..model.billable_type import BillableType


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT)
    amount_total = models.IntegerField(default=0)
    detail = models.TextField(null=True, blank=True)
class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = [
            'invoice',
            'amount_total',
        ]


