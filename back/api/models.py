from django.db import models
from django.utils import timezone
import pytz

timezone.activate(pytz.timezone('UTC'))


class Client(models.Model):
    name = models.CharField(max_length=64)


class WorkInterval(models.Model):
    start = models.DateTimeField()
    stop = models.DateTimeField(null=True)
    start_utcms = models.BigIntegerField(null=True)
    stop_utcms = models.BigIntegerField(null=True)
    description = models.TextField(null=True, blank=True)
    client = models.ForeignKey(Client, null=False, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        if isinstance(self.start, str):
            utc = timezone.datetime.fromisoformat(self.start)
        else:
            utc = self.start
        self.start_utcms = round(utc.timestamp())
        if self.stop:
            if isinstance(self.stop, str):
                utc = timezone.datetime.fromisoformat(self.stop)
            else:
                utc = self.stop
            self.stop_utcms = round(utc.timestamp())
        super(WorkInterval, self).save(*args, **kwargs)
