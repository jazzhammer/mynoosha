import json

import requests

endpoint_clients = 'http://localhost:8001/api/v0/clients/'
TEST_NAME = 'testingONLY'


def test_get():
    createClient(TEST_NAME)
    deleteClientsForName(TEST_NAME)
    founds = getClientsForName(TEST_NAME)
    assert founds is None

def createClient(name):
    response = requests.post(endpoint_clients, json={'name': TEST_NAME})
    assert response.status_code == 201
    return json.loads(response.content.decode('utf8'))

def getClientsForName(name):
    response = requests.get(endpoint_clients, params={'search': name})
    if response.status_code == 200:
        content = response.content.decode('utf8')
        founds = json.loads(content)
        return founds
    else:
        return None

def deleteClientsForName(name):
    founds = getClientsForName(name)
    for found in founds:
        response = requests.delete(endpoint_clients, params={'id': found['id']})
        assert response.status_code == 200
    response = requests.get(endpoint_clients, params={'search': name})
    assert response.status_code == 404
