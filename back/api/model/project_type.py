from django.db import models
from rest_framework import serializers

class ProjectType(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        indexes = [models.Index(fields=['name'])]

class ProjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectType

        fields = [
            'name'
        ]