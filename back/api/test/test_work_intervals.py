import os

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
    # ============================================================
    # get a client, for all tests
    # ============================================================
    response = requests.get(endpoint_clients, params={'search': TEST_NAME})
    if response.status_code != 200:
        response = requests.post(endpoint_clients, json={'name': TEST_NAME})
        assert response.status_code == 201
        found = json.loads(json.loads(response.content))
    else:
        content = response.content.decode('utf8')
        founds = json.loads(json.loads(content))
        found = founds[0]
    # ============================================================
    # CRUD, with getting by id only
    # ============================================================
    dt_str = str(timezone.now() - timezone.timedelta(hours=1))
    post_parms = {
        'start': dt_str,
        'client': found['id'],
        'description': 'a test interval'
    }
    response = requests.post(endpoint_work_intervals, json=post_parms)
    assert response.status_code == 201
    created = json.loads(response.content.decode('utf8'))
    created['stop'] = str(timezone.now())
    edited = created
    response = requests.put(endpoint_work_intervals, json=edited)
    assert response.status_code == 200
    response = requests.delete(endpoint_work_intervals, params={'id': created['id']})
    assert response.status_code == 200
    response = requests.get(endpoint_work_intervals, params={'id': created['id']})
    assert response.status_code == 404
    # ============================================================
    # cRud, with getting by datetime boundaries
    # ============================================================
    # interval 1 hour ago
    dt_str = str(timezone.now() - timezone.timedelta(hours=1))
    post_parms = {
        'start': dt_str,
        'client': found['id'],
        'description': 'a test interval'
    }
    response = requests.post(endpoint_work_intervals, json=post_parms)
    assert response.status_code == 201
    created = json.loads(response.content.decode('utf8'))
    hours_ago_2 = timezone.now() - timezone.timedelta(hours=2)
    response = requests.get(endpoint_work_intervals, params={'pre_start': str(hours_ago_2)})
    assert response.status_code == 200
    founds = json.loads(response.content)
    assert len([instance for instance in founds if instance['id'] == created['id']]) > 0
    hour_from_now_2 = timezone.now() + timezone.timedelta(hours=2)
    response = requests.get(endpoint_work_intervals, params={'pre_start': str(hour_from_now_2)})
    assert response.status_code == 200
    founds = json.loads(response.content)
    assert len([instance for instance in founds if instance['id'] == created['id']]) == 0
