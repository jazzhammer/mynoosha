from django.db import models
from django.utils import timezone
import pytz

timezone.activate(pytz.timezone('UTC'))


class Client(models.Model):
    name = models.CharField(max_length=64)
    address_street = models.CharField(max_length=64, null=True, blank=True)
    address_city = models.CharField(max_length=64, null=True, blank=True)
    address_province_state = models.CharField(max_length=32, null=True, blank=True)
    address_postal_zip_code = models.CharField(max_length=7, null=True, blank=True)

class WorkInterval(models.Model):
    # id = modelObjectIdField(db_column="_id", primary_key=True)
    start = models.DateTimeField()
    stop = models.DateTimeField(null=True)
    start_utcms = models.BigIntegerField(null=True)
    stop_utcms = models.BigIntegerField(null=True)
    description = models.TextField(null=True, blank=True)
    client = models.ForeignKey(Client, null=False, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        if isinstance(self.start, str):
            if self.start.endswith('Z'):
                self.start = self.start[:-1]
            utc = timezone.datetime.fromisoformat(self.start)
        else:
            utc = self.start
        self.start_utcms = round(utc.timestamp())
        if self.stop:
            if isinstance(self.stop, str):
                if self.stop.endswith('Z'):
                    self.stop = self.stop[:-1]
                utc = timezone.datetime.fromisoformat(self.stop)
            else:
                utc = self.stop
            self.stop_utcms = round(utc.timestamp())
        super(WorkInterval, self).save(*args, **kwargs)
