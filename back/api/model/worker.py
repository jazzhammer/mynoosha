from django.db import models
from rest_framework import serializers

class Worker(models.Model):
    last_name = models.CharField(max_length=64)
    first_name = models.CharField(max_length=64)

def get_default_worker():
    defaults = Worker.objects.filter(last_name='default', first_name='worker')
    if defaults.count() == 0:
        default = Worker(last_name='default', first_name='worker')
        default.save()
    else:
        default = defaults.first()
    return default

class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = [
            'last_name',
            'first_name'
        ]