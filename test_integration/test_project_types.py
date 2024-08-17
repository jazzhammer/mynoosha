import json

import requests

endpoint_project_types = 'http://localhost:8001/api/v0/project_types/'
TEST_NAME = 'testingONLY'

def test_get():
    deleteProjectTypesForName(TEST_NAME)
    created = createProjectType(
        TEST_NAME
    )
    deleteProjectTypesForName(created.get('name'))
    founds = getProjectTypesForName(TEST_NAME)
    assert founds == []

def createProjectType(name):
    response = requests.post(endpoint_project_types, json={
        'name': name
    })
    assert response.status_code == 201

    created = json.loads(response.content.decode('utf8'))
    assert created.get('name') == name
    return created

def get_project_type_for_name(name):
    response = requests.get(endpoint_project_types, params={'name': name})
    if response.status_code == 200:
        content = response.content.decode('utf8')
        found = json.loads(content)[0]
        return found
    else:
        return None

def getProjectTypesForName(name):
    response = requests.get(endpoint_project_types, params={'search': name})
    if response.status_code == 200:
        content = response.content.decode('utf8')
        founds = json.loads(content)
        return founds
    else:
        return None

def deleteProjectTypesForName(name):
    founds = getProjectTypesForName(name)
    for found in founds:
        response = requests.delete(endpoint_project_types, params={'id': found['id']})
        assert response.status_code == 200
    response = requests.get(endpoint_project_types, params={'search': name})
    assert response.status_code == 200
