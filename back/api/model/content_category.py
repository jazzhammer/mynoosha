from django.db import models
from rest_framework import serializers

class ContentCategory(models.Model):
    name = models.CharField(max_length=128)



class ContentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentCategory

        fields=[
            'name'
        ]