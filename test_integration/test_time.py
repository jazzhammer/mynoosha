import requests
from datetime import timedelta, timezone
import datetime
from .utils.time_utils import utc_dt, utc_ts

endpoint_time_utils_utc_string = 'http://localhost:8001/api/v0/utils/time/utc_string/'
endpoint_time_utils_utc_timestamp = 'http://localhost:8001/api/v0/utils/time/utc_timestamp/'


def test_time():
    utc_dt_now = utc_dt()
    print(f"{utc_dt_now=}")
    utc_dt_minus = utc_dt(-3)
    print(f"{utc_dt_minus=}")
    utc_dt_minus = utc_dt(-3, -2)
    print(f"{utc_dt_minus=}")
    utc_dt_minus = utc_dt(-3, -2, -1)
    print(f"{utc_dt_minus=}")
    utc_dt_iso = utc_dt(iso_format='2024-07-24 12:27:03.646000 +00:00')
    print(f"{utc_dt_iso=}")

    utc_ts_now = utc_ts()
    print(f"{utc_ts_now=}")
    utc_ts_minus = utc_ts(-3)
    print(f"{utc_ts_minus=}")
    utc_ts_minus = utc_ts(-3, -2)
    print(f"{utc_ts_minus=}")
    utc_ts_minus = utc_ts(-3, -2, -1)
    print(f"{utc_ts_minus=}")
    utc_ts_iso = utc_ts(iso_format='2024-07-24 12:27:03.646000 +00:00')
    print(f"{utc_ts_iso=}")
