import json
from datetime import datetime

import requests

endpoint_clients = 'http://localhost:8001/api/v0/clients/'
endpoint_work_intervals = 'http://localhost:8001/api/v0/work_intervals/'
TEST_NAME = 'busyclient'


def test_post_delete():
    # get a client
    response = requests.get(endpoint_clients, params={'search': TEST_NAME})
    if response.status_code != 200:
        response = requests.post(endpoint_clients, json={'name': TEST_NAME})
        assert response.status_code == 201
        found = json.loads(json.loads(response.content))
    else:
        content = response.content.decode('utf8')
        founds = json.loads(json.loads(content))
        found = founds[0]
    dt_str = str(datetime.now())
    post_parms = {
        'start': dt_str,
        'client': found['id'],
        'description': 'a test interval'
    }
    response = requests.post(endpoint_work_intervals, json=post_parms)
    assert response.status_code == 201
    created = json.loads(response.content.decode('utf8'))
    response = requests.delete(endpoint_work_intervals, params={'id': created['id']})
    assert response.status_code == 200
