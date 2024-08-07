import json

import requests

endpoint_billable_types = 'http://localhost:8001/api/v0/billable_types/'
TEST_NAME = 'testingBTONLY'

def test_get():
    created = create_billable_type(
        TEST_NAME
    )
    delete_billable_type_for_name(created.get('name'))
    founds = get_billable_type_for_name(TEST_NAME)
    assert founds is None

def create_billable_type(
        name
    ):
    response = requests.post(endpoint_billable_types, json={
        'name': name
    })
    assert response.status_code == 201

    created = json.loads(response.content.decode('utf8'))
    assert created.get('name') == name
    return created

def get_billable_type_for_name(name):
    response = requests.get(endpoint_billable_types, params={'search': name})
    if response.status_code == 200:
        content = response.content.decode('utf8')
        founds = json.loads(content)
        return founds
    else:
        return None

def delete_billable_type_for_name(name):
    founds = get_billable_type_for_name(name)
    for found in founds:
        response = requests.delete(endpoint_billable_types, params={'id': found['id']})
        assert response.status_code == 200
    response = requests.get(endpoint_billable_types, params={'search': name})
    assert response.status_code == 404
