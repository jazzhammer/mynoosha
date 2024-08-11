import json
from datetime import datetime

import requests

endpoint_workers = 'http://localhost:8001/api/v0/workers/'
endpoint_utc_iso = 'http://localhost:8001/api/v0/utc/iso'
TEST_LAST_NAME = 'testLastName'
TEST_FIRST_NAME = 'testFirstName'


def test_get():
    response = requests.get(endpoint_utc_iso, params={'iso_format': '2012-08-11 16:30:22.841663 +00:00'})
    decoded = response.content.decode('utf8')
    decoded = decoded.replace('"', '').replace("'", "")
    ymd_birth = datetime.fromisoformat(decoded)

    deleteWorkersForNames(TEST_LAST_NAME, TEST_FIRST_NAME)

    created = create_worker(
        TEST_LAST_NAME,
        TEST_FIRST_NAME,
        ymd_birth
    )
    assert created.get('last_name') == TEST_LAST_NAME
    assert created.get("first_name") == TEST_FIRST_NAME
    deleteWorkersForNames(TEST_LAST_NAME, TEST_FIRST_NAME)

def create_worker(
        last_name,
        first_name,
        ymd_birth
):
    response = requests.post(endpoint_workers, json={
        'last_name': last_name,
        'first_name': first_name,
        'ymd_birth': ymd_birth.isoformat()
    })
    assert response.status_code == 201

    created = json.loads(response.content.decode('utf8'))
    assert created.get('first_name') == first_name
    assert created.get('last_name') == last_name
    created_ymd_birth = created.get("ymd_birth")
    assert created_ymd_birth == ymd_birth.isoformat()[:len(created_ymd_birth)]
    return created


def get_worker_for_name(name):
    response = requests.get(endpoint_workers, params={'name': name})
    if response.status_code == 200:
        content = response.content.decode('utf8')
        found = json.loads(content)[0]
        return found
    else:
        return None


def getWorkersForNames(last_name, first_name):
    response = requests.get(endpoint_workers, params={'last_name': last_name, 'first_name': first_name})
    if response.status_code == 200:
        content = response.content.decode('utf8')
        founds = json.loads(content)
        return founds
    else:
        return None


def deleteWorkersForNames(last_name, first_name):
    founds = getWorkersForNames(last_name, first_name)
    for found in founds:
        response = requests.delete(endpoint_workers, params={'id': found['id']})
        assert response.status_code == 200
    founds = getWorkersForNames(last_name, first_name)
    assert len(founds) == 0
