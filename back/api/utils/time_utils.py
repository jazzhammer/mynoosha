from datetime import timezone, timedelta
import datetime


def utc_dt(*args, **kwargs):
    days_offset = kwargs.get('days_offset')
    hours_offset = kwargs.get('hours_offset')
    minutes_offset = kwargs.get('minutes_offset')
    iso_format = kwargs.get('iso_format')
    if iso_format is None and len(args) > 0:
        iso_format  = args[0]
    if days_offset is None and len(args) >= 1:
        days_offset = args[0]
        if days_offset is None:
            days_offset = kwargs.get('days_offset')

    if hours_offset is None and len(args) >= 2:
        hours_offset = args[1]
        if hours_offset is None:
            hours_offset = kwargs.get('hours_offset')

    if minutes_offset is None and len(args) >= 3:
        minutes_offset = args[2]
        if minutes_offset is None:
            minutes_offset = kwargs.get('minutes_offset')

    utc_dt_next = datetime.datetime.now(timezone.utc)
    if days_offset is not None:
        utc_dt_next = utc_dt_next + timedelta(days=days_offset)
    if hours_offset is not None:
        utc_dt_next = utc_dt_next + timedelta(hours=hours_offset)
    if minutes_offset is not None:
        utc_dt_next = utc_dt_next + timedelta(minutes=minutes_offset)
    if iso_format is not None:
        if 'Z' in iso_format:
            iso_format = iso_format[:iso_format.index('Z')]
        if '+' in iso_format:
            iso_format = iso_format[:iso_format.index('+')]
        iso_format = iso_format.strip()
        utc_dt_next = datetime.datetime.fromisoformat(iso_format)
    return utc_dt_next

def utc_ts(*args, **kwargs):
    dt = utc_dt(*args, **kwargs)
    return dt.timestamp()
