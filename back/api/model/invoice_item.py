from rest_framework import serializers
from django.db import models

from .work_type import WorkType
from .invoice import Invoice


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT)
    amount_total = models.IntegerField(default=0)
    detail = models.TextField(null=True, blank=True)
    work_type = models.ForeignKey(WorkType, null=True, on_delete=models.PROTECT)

class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = [
            'invoice',
            'amount_total',
        ]


