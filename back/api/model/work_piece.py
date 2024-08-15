from django.db.models import Model
from django.db import models
from rest_framework import serializers

from api.model import Worker, Client
from api.model.invoice_item import InvoiceItem


class WorkPiece(Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    start = models.DateTimeField()
    invoice_item = models.ForeignKey(InvoiceItem, null=True, on_delete=models.PROTECT)
    worker = models.ManyToManyField(Worker)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)

    class Meta:
        indexes = [models.Index(fields=['start'])]

class WorkPieceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkPiece
        fields = [
            'name',
            'description',
            'start',
            'client'
        ]