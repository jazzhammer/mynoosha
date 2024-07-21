from django.db import models


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
        self.start_utcms = round(self.start.timestamp())
        self.stop_utcms = round(self.start.timestamp())
        print(f'calculated {self.start_utcms}')
        print(f'calculated {self.stop_utcms}')
        super(WorkInterval, self).save(*args, **kwargs)
