import json

import requests

endpoint_clients = 'http://localhost:8001/api/v0/clients/'
TEST_NAME = 'testingONLY'
TEST_ADDRESS_STREET = 'testStreet'
TEST_ADDRESS_CITY = 'testCity'
TEST_ADDRESS_PROVINCE_STATE = 'testProvinceState'
TEST_ADDRESS_POSTAL_ZIP_CODE = '1234567'

def test_get():
    created = createClient(
        TEST_NAME,
        TEST_ADDRESS_STREET,
        TEST_ADDRESS_CITY,
        TEST_ADDRESS_PROVINCE_STATE,
        TEST_ADDRESS_POSTAL_ZIP_CODE
    )
    deleteClientsForName(created.get('name'))
    founds = getClientsForName(TEST_NAME)
    assert founds is None

def createClient(
        name,
        test_address_street,
        test_address_city,
        test_address_province_state,
        test_address_postal_zip_code
    ):
    response = requests.post(endpoint_clients, json={
        'name': name,
        'address_street': test_address_street,
        'address_city': test_address_city,
        'address_province_state': test_address_province_state,
        'address_postal_zip_code': test_address_postal_zip_code,
    })
    assert response.status_code == 201

    created = json.loads(response.content.decode('utf8'))
    assert created.get('name') == name
    assert created.get('address_street') == test_address_street
    assert created.get('address_city') == test_address_city
    assert created.get('address_province_state') == test_address_province_state
    assert created.get('address_postal_zip_code') == test_address_postal_zip_code
    return created

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
