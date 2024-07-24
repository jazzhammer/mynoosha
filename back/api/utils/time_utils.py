from django.utils import timezone
import pytz

timezone.activate(pytz.timezone('UTC'))


def get_utc_timestamp(*args):
    if len(args) == 0:
        source = str(timezone.now())
    else:
        source = args[0]
    if source.endswith('Z'):
        source = source.replace('Z', '+00:00')
    return timezone.datetime.fromisoformat(source).timestamp()

def get_utc_string(*args):
    if len(args) == 0:
        return str(timezone.now())
    source = args[0]
    if source.endswith('Z'):
        source = source.replace('Z', '+00:00')
    return timezone.datetime.fromisoformat(source)
