import json

import requests

endpoint_projects = 'http://localhost:8001/api/v0/projects/'
TEST_NAME = 'testingONLY'
TEST_DESCRIPTION = 'testDescription'

def test_get():
    created = create_project(
        TEST_NAME,
        TEST_DESCRIPTION,
    )
    delete_projects_for_name(created.get('name'))
    founds = get_projects_for_name(TEST_NAME)
    assert founds == []

def create_project(
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

def get_projects_for_name(name):
    response = requests.get(endpoint_projects, params={'search': name})
    if response.status_code == 200:
        content = response.content.decode('utf8')
        founds = json.loads(content)
        return founds
    else:
        return None

def delete_projects_for_name(name):
    founds = get_projects_for_name(name)
    for found in founds:
        response = requests.delete(endpoint_projects, params={'id': found['id']})
        assert response.status_code == 200
    response = requests.get(endpoint_projects, params={'search': name})
    assert response.status_code == 200
    founds = json.loads(response.content.decode('utf8'))
    assert len(founds) == 0
