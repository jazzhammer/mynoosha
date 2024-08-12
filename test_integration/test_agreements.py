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
    client = create_default_client()
    worker = create_default_worker()
    response = requests.post(endpoint_agreements, data={
        'client': client.get('id'),
        'worker': worker.get('id'),
        'name': TEST_PROJECT_NAME_1
    })
    assert response.status_code == 201
    agreement = json.loads(response.content.decode('utf8'))
    # update with missing id
    response = requests.put(endpoint_agreements, data={
        'client': client.get('id'),
        'worker': worker.get('id'),
        'name': TEST_PROJECT_NAME_1
    })
    assert response.status_code == 400

    # update with another client
    client = create_client_for_name('testName444')
    response = requests.put(endpoint_agreements, data={
        'id': agreement.get('id'),
        'client': client.get('id'),
        'worker': worker.get('id'),
        'name': TEST_AGREEMENT_NAME_1
    })
    assert response.status_code == 200
    updated = json.loads(response.content.decode('utf8'))
    assert updated.get('client') == client.get('id')
    assert updated.get('worker') == worker.get('id')
    assert updated.get('name') == TEST_AGREEMENT_NAME_1

    # change worker
    worker = create_worker_with_names('left', 'right')
    response = requests.put(endpoint_agreements, data={
        'id': agreement.get('id'),
        'client': client.get('id'),
        'worker': worker.get('id'),
        'name': TEST_AGREEMENT_NAME_1
    })
    assert response.status_code == 200
    updated = json.loads(response.content.decode('utf8'))
    assert updated.get('client') == client.get('id')
    assert updated.get('worker') == worker.get('id')
    assert updated.get('name') == TEST_AGREEMENT_NAME_1

    # change agreement name
    worker = create_worker_with_names('another last', 'another first')
    response = requests.put(endpoint_agreements, data={
        'id': agreement.get('id'),
        'client': client.get('id'),
        'worker': worker.get('id'),
        'name': TEST_AGREEMENT_NAME_2
    })
    assert response.status_code == 200
    updated = json.loads(response.content.decode('utf8'))
    assert updated.get('client') == client.get('id')
    assert updated.get('worker') == worker.get('id')
    assert updated.get('name') == TEST_AGREEMENT_NAME_2

def get_agreements_for_worker(worker):
    response = requests.get(endpoint_agreements, params={'worker': worker.get("id")})
    assert response.status_code == 200
    return json.loads(response.content.decode('utf8'))