import json

import requests

endpoint_invoices = 'http://localhost:8001/api/v0/invoices/'
TEST_NAME = 'testingONLY'
TEST_DESCRIPTION = 'testDescription'

def test_get():
    created = createInvoice(
        TEST_NAME,
        TEST_DESCRIPTION,
    )
    deleteInvoicesForName(created.get('name'))
    founds = getInvoicesForName(TEST_NAME)
    assert founds is None

def createInvoice(
        name,
        test_description
    ):
    response = requests.post(endpoint_invoices, json={
        'name': name,
        'description': test_description
    })
    assert response.status_code == 201

    created = json.loads(response.content.decode('utf8'))
    assert created.get('name') == name
    assert created.get('description') == test_description
    return created

def getInvoicesForName(name):
    response = requests.get(endpoint_invoices, params={'search': name})
    if response.status_code == 200:
        content = response.content.decode('utf8')
        founds = json.loads(content)
        return founds
    else:
        return None

def deleteInvoicesForName(name):
    founds = getInvoicesForName(name)
    for found in founds:
        response = requests.delete(endpoint_invoices, params={'id': found['id']})
        assert response.status_code == 200
    response = requests.get(endpoint_invoices, params={'search': name})
    assert response.status_code == 404
