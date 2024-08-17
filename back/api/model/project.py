from rest_framework import serializers
from django.db import models

from ..model.agreement import Agreement


class Project(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(null=True)
    agreement = models.ForeignKey(Agreement, null=True, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now=True)

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'name',
            'agreement',
            "description"
        ]
