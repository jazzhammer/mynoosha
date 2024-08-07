from rest_framework import serializers
from django.db import models
from .worker import Worker

class Client(models.Model):
    name = models.CharField(max_length=64)
    address_street = models.CharField(max_length=64, null=True, blank=True)
    address_city = models.CharField(max_length=64, null=True, blank=True)
    address_province_state = models.CharField(max_length=32, null=True, blank=True)
    address_postal_zip_code = models.CharField(max_length=7, null=True, blank=True)
    workers = models.ManyToManyField(Worker)

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            'name',
            'address_street',
            'address_city',
            'address_province_state',
            'address_postal_zip_code',
        ]
