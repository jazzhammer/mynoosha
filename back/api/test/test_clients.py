import json

import requests

endpoint_clients = 'http://localhost:8001/api/v0/clients/'
TEST_NAME = 'asdf'


def test_get():
    # delete if exists
    response = requests.get(endpoint_clients, params={'search': TEST_NAME})
    if response.status_code == 200:
        content = response.content.decode('utf8')
        founds = json.loads(json.loads(content))
        requests.delete(endpoint_clients, params={'id': founds[0]['id']})
    response = requests.get(endpoint_clients, params={'search': TEST_NAME})
    assert response.status_code != 200
    # post
    response = requests.post(endpoint_clients, json={'name': TEST_NAME})
    assert response.status_code == 201
    response = requests.get(endpoint_clients, params={'search': TEST_NAME})
    assert response.status_code == 200
