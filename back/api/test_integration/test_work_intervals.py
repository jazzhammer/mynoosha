import os

from .utils.time_utils import get_utc_timestamp

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "back.settings")

import django

django.setup()

from django.core.management import call_command

import json
from datetime import datetime
from django.utils.timezone import make_aware as UTC
import requests

endpoint_clients = 'http://localhost:8001/api/v0/clients/'
endpoint_work_intervals = 'http://localhost:8001/api/v0/work_intervals/'
TEST_NAME = 'busyclient'

from django.utils import timezone
import pytz

timezone.activate(pytz.timezone('UTC'))

def test_crud():
    client = confirmClientExists()
    deleteClientWorkIntervals(client)
    created = createClientWorkIntervals(client, 1)[0]
    updated = updateWorkIntervalStop(created)
    deleteWorkIntervalById(updated)
    createClientWorkIntervals(client, 3)
    readClientWorkIntervals(client, 3)
    deleteClientWorkIntervals(client)
    # ============================================================
    # cRud, with getting by datetime boundaries
    # ============================================================
    created = createClientWorkIntervals(client, 1)[0]
    founds = readWorkIntervals(hours_ago=2)
    assert len([instance for instance in founds if instance['id'] == created['id']]) > 0
    founds = readWorkIntervals(hours_ahead=2)
    assert len([instance for instance in founds if instance['id'] == created['id']]) == 0

def deleteClientWorkIntervals(client):
    response = requests.get(endpoint_work_intervals, params={'client': client['id']})
    assert response.status_code == 200
    founds = json.loads(response.content.decode('utf8'))
    for found in founds:
        requests.delete(endpoint_work_intervals, params={'id': found['id']})
    response = requests.get(endpoint_work_intervals, params={'client': client['id']})
    assert response.status_code == 200
    founds = json.loads(response.content.decode('utf8'))
    assert not founds or len(founds) == 0

def createClientWorkIntervals(client, qty):
    createds = []
    for w in range(qty):
        dt_str = str(timezone.now() - timezone.timedelta(hours=1))
        post_parms = {
            'start': dt_str,
            'client': client['id'],
            'description': 'a test interval'
        }
        response = requests.post(endpoint_work_intervals, json=post_parms)
        created = json.loads(response.content.decode('utf8'))
        assert created
        assert response.status_code == 201
        createds.append(created)
    print(f"created WorkIntervals({len(createds)=}) for Client[{client['id']=}]")
    return createds

def readClientWorkIntervals(client, expected_qty):
    response = requests.get(endpoint_work_intervals, params={'client': client['id']})
    assert response.status_code == 200
    founds = json.loads(response.content.decode('utf8'))
    assert len(founds) == 3

def updateWorkIntervalStop(interval):
    next_stop = str(timezone.now())
    interval['stop'] = next_stop
    edited = interval
    response = requests.put(endpoint_work_intervals, json=edited)
    assert response.status_code == 200
    updated = json.loads(response.content.decode('utf8'))
    assert updated['stop'] == next_stop
    utc_ts = round(get_utc_timestamp(next_stop))
    assert updated.get('stop_utcms') == utc_ts
    return updated

def deleteWorkIntervalById(interval):
    response = requests.delete(endpoint_work_intervals, params={'id': interval['id']})
    assert response.status_code == 200
    response = requests.get(endpoint_work_intervals, params={'id': interval['id']})
    assert response.status_code == 404

def confirmClientExists():
    response = requests.get(endpoint_clients, params={'search': TEST_NAME})
    if response.status_code != 200:
        response = requests.post(endpoint_clients, json={'name': TEST_NAME})
        assert response.status_code == 201
        found = json.loads(json.loads(response.content))
    else:
        content = response.content.decode('utf8')
        founds = json.loads(json.loads(content))
        found = founds[0]
    return found

def readWorkIntervals(*args, **kwargs):
    hours_ago = kwargs.get('hours_ago')
    hours_ahead = kwargs.get('hours_ahead')
    if hours_ago and hours_ahead:
        raise Exception(f"unable to look in past and future at the same time: {hours_ago=}, {hours_ahead=}")
    if hours_ago:
        ago_delta = timezone.now() - timezone.timedelta(hours=hours_ago)
    if hours_ahead:
        ago_delta = timezone.now() + timezone.timedelta(hours=hours_ahead)

    response = requests.get(endpoint_work_intervals, params={'pre_start': str(ago_delta)})
    assert response.status_code == 200
    loadable = response.content
    if isinstance(loadable, str):
        return json.loads(loadable)
    else:
        return json.loads(loadable.decode('utf8'))

