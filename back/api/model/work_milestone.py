from django.db.models import Model
from django.db import models
from rest_framework import serializers

from api.model import Worker, Client, Project
from api.model.invoice_item import InvoiceItem


class WorkMilestone(Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    start = models.DateTimeField(null=True)
    invoice_item = models.ForeignKey(InvoiceItem, null=True, on_delete=models.PROTECT)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    workers = models.ManyToManyField(Worker)

    class Meta:
        indexes = [models.Index(fields=['start'])]

class WorkMilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkMilestone
        fields = [
            'name',
            'description',
            # 'start',
            'client',
            'project',
            # 'worker',
        ]