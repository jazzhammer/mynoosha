from django.db.models import Model
from django.db import models
from rest_framework import serializers

from api.model import Worker, Client, Project
from api.model.invoice_item import InvoiceItem


class WorkPiece(Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    start = models.DateTimeField()
    finish = models.DateTimeField()
    invoice_item = models.ForeignKey(InvoiceItem, null=True, on_delete=models.PROTECT)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    worker = models.ManyToManyField(Worker)

    class Meta:
        indexes = [models.Index(fields=['start'])]

class WorkPieceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkPiece
        fields = [
            'name',
            'description',
            'start',
            'finish',
            'client',
            'project',
            'worker',
        ]