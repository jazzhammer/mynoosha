from django.db import models
from rest_framework import serializers

"""
eg, name='time' | 'piece' | 'milestone'
"""
class WorkType(models.Model):
    name = models.CharField(max_length=24)
    description = models.TextField(null=True, blank=True, default='')

    class Meta:
        indexes = [models.Index(fields=['name'])]

class WorkTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkType

        fields = [
            'name',
            'description'
        ]