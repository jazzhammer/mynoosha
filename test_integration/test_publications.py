import json

import requests

endpoint_publications = 'http://localhost:8001/api/v0/publications/'
TEST_TITLE = 'testingONLY'

def test_get():
    created = createPublication(
        TEST_TITLE
    )
    deletePublicationsForTitle(created.get('title'))
    founds = getPublicationsForTitle(TEST_TITLE)
    assert founds is None

def createPublication(
        title,
        test_address_street,
        test_address_city,
        test_address_province_state,
        test_address_postal_zip_code
    ):
    response = requests.post(endpoint_publications, json={
        'title': title,
        'address_street': test_address_street,
        'address_city': test_address_city,
        'address_province_state': test_address_province_state,
        'address_postal_zip_code': test_address_postal_zip_code,
    })
    assert response.status_code == 201

    created = json.loads(response.content.decode('utf8'))
    assert created.get('title') == title
    assert created.get('address_street') == test_address_street
    assert created.get('address_city') == test_address_city
    assert created.get('address_province_state') == test_address_province_state
    assert created.get('address_postal_zip_code') == test_address_postal_zip_code
    return created

def getPublicationsForTitle(title):
    response = requests.get(endpoint_publications, params={'search': title})
    if response.status_code == 200:
        content = response.content.decode('utf8')
        founds = json.loads(content)
        return founds
    else:
        return None

def deletePublicationsForTitle(title):
    founds = getPublicationsForTitle(title)
    for found in founds:
        response = requests.delete(endpoint_publications, params={'id': found['id']})
        assert response.status_code == 200
    response = requests.get(endpoint_publications, params={'search': title})
    assert response.status_code == 404
