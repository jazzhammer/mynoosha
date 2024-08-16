import json

import requests

from test_integration.test_clients import create_default_client, delete_client, create_client_for_name
from test_integration.test_workers import create_default_worker, delete_worker, create_worker_with_names

endpoint_agreements = 'http://localhost:8001/api/v0/agreements/'
TEST_PROJECT_NAME_1 = "testProjectName1"
TEST_PROJECT_NAME_2 = "testProjectName2"
TEST_AGREEMENT_NAME_1 = "testAgreementName1"
TEST_AGREEMENT_NAME_2 = "testAgreementName2"


def test_get():
    created = create_default_agreement()
    update_agreement_client(created)
    update_agreement_worker(created)
    update_agreement_name(created)
    delete_agreements_for_name(TEST_AGREEMENT_NAME_1)
    delete_agreements_for_name(TEST_AGREEMENT_NAME_2)


def update_agreement_name(agreement):
    response = requests.put(endpoint_agreements, data={
        'id': agreement.get('id'),
        'client': agreement.get('client'),
        'worker': agreement.get('worker'),
        'name': TEST_AGREEMENT_NAME_2
    })
    assert response.status_code == 200
    updated = json.loads(response.content.decode('utf8'))
    assert updated.get('client') == agreement.get('client')
    assert updated.get('worker') == agreement.get('worker')
    assert updated.get('name') == TEST_AGREEMENT_NAME_2


def update_agreement_worker(agreement):
    worker = create_worker_with_names('left', 'right')
    response = requests.put(endpoint_agreements, data={
        'id': agreement.get('id'),
        'client': agreement.get('client'),
        'worker': worker.get('id'),
        'name': TEST_AGREEMENT_NAME_1
    })
    assert response.status_code == 200
    updated = json.loads(response.content.decode('utf8'))
    assert updated.get('client') == agreement.get('client')
    assert updated.get('worker') == worker.get('id')
    assert updated.get('name') == TEST_AGREEMENT_NAME_1


def update_agreement_client(agreement):
    client = create_client_for_name('testName444')
    response = requests.put(endpoint_agreements, data={
        'id': agreement.get('id'),
        'client': client.get('id'),
        'worker': agreement.get('worker'),
        'name': TEST_AGREEMENT_NAME_1
    })
    assert response.status_code == 200
    updated = json.loads(response.content.decode('utf8'))
    assert updated.get('client') == client.get('id')
    assert updated.get('worker') == agreement.get('id')
    assert updated.get('name') == TEST_AGREEMENT_NAME_1


def delete_agreements_for_name(name):
    agreements = get_agreements_for_name(name)
    for agreement in agreements:
        requests.delete(endpoint_agreements, params={'id': agreement.get('id')})
    agreements = get_agreements_for_name(name)
    assert len(agreements) == 0


def delete_agreement(agreement):
    requests.delete(endpoint_agreements, params={'id': agreement.get('id')})
    found = get_agreement_for_id(agreement.get('id'))
    assert found == None


def get_agreements_for_name(name):
    response = requests.get(endpoint_agreements, params={'name': name})
    return json.loads(response.content.decode('utf8'))


def get_agreement_for_id(id):
    response = requests.get(endpoint_agreements, params={'id': id})
    if response.status_code == 200:
        return json.loads(response.content.decode('utf8'))
    else:
        return None


def get_agreements_for_worker(worker):
    response = requests.get(endpoint_agreements, params={'worker': worker.get("id")})
    assert response.status_code == 200
    return json.loads(response.content.decode('utf8'))


def create_default_agreement():
    client = create_default_client()
    worker = create_default_worker()
    return create_agreement(client, worker)


def create_agreement(client, worker):
    response = requests.post(endpoint_agreements, data={
        'client': client.get('id'),
        'worker': worker.get('id'),
        'name': TEST_PROJECT_NAME_1
    })
    assert response.status_code == 201
    agreement = json.loads(response.content.decode('utf8'))
    return agreement
