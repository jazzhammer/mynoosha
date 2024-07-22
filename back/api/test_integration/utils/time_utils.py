from django.utils import timezone
import pytz

timezone.activate(pytz.timezone('UTC'))


def get_utc_timestamp(source):
    if source.endswith('Z'):
        source = source[:-1]
    return timezone.datetime.fromisoformat(source).timestamp()
