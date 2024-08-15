from django.db import models
from rest_framework import serializers

from api.model.work_piece import WorkPiece

"""
"""
class Medium(models.Model):
    name = models.CharField(max_length=24, null=True, blank=True)
    url = models.URLField(null=True)
    work_piece = models.ManyToManyField(WorkPiece)
    filename = models.CharField(max_length=128)
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
class MediumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medium

        fields = [
            'name',
            'url',
            'filename'
        ]