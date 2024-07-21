from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=64)


class WorkInterval(models.Model):
    start = models.DateTimeField()
    stop = models.DateTimeField(null=True)
    description = models.TextField(null=True, blank=True)
    client = models.ForeignKey(Client, null=False, on_delete=models.PROTECT)
