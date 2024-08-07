import json

import requests

endpoint_projects = 'http://localhost:8001/api/v0/work_types/'
TEST_NAME = 'testingONLY'
TEST_DESCRIPTION = 'testDescription'

def test_get():
    created = createWorkType(
        TEST_NAME,
        TEST_DESCRIPTION,
    )
    deleteWorkTypesForName(created.get('name'))
    founds = getWorkTypesForName(TEST_NAME)
    assert founds is None

def createWorkType(
        name,
        test_description
    ):
    response = requests.post(endpoint_projects, json={
        'name': name,
        'description': test_description
    })
    assert response.status_code == 201

    created = json.loads(response.content.decode('utf8'))
    assert created.get('name') == name
    assert created.get('description') == test_description
    return created

def getWorkTypesForName(name):
    response = requests.get(endpoint_projects, params={'search': name})
    if response.status_code == 200:
        content = response.content.decode('utf8')
        founds = json.loads(content)
        return founds
    else:
        return None

def deleteWorkTypesForName(name):
    founds = getWorkTypesForName(name)
    for found in founds:
        response = requests.delete(endpoint_projects, params={'id': found['id']})
        assert response.status_code == 200
    response = requests.get(endpoint_projects, params={'search': name})
    assert response.status_code == 404
