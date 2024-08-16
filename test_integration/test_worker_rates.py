import json

import requests

from test_integration.test_agreements import create_default_agreement, delete_agreement
from test_integration.test_workers import get_worker_for_id

endpoint_worker_rates = 'http://localhost:8001/api/v0/worker_rates/'

def test_get():
    agreement = create_default_agreement()
    worker = get_worker_for_id(agreement.get('worker'))
    created = create_worker_rate(
        worker,
        agreement
    )
    update_amount_rate(created, 888)
    delete_worker_rate(created)
    delete_agreement(agreement)

def update_amount_rate(worker_rate, next_amount):
    worker_rate['amount_rate'] = next_amount
    response = requests.put(endpoint_worker_rates, data={**worker_rate})
    assert response.status_code == 200
    updated = json.loads(response.content.decode('utf8'))
    assert updated.get('amount_rate') == next_amount

def create_worker_rate(worker, agreement):
    amount_rate = 100
    response = requests.post(endpoint_worker_rates, data={
        "worker": worker.get('id'),
        "agreement": agreement.get('id'),
        "amount_rate": amount_rate
    })
    assert response.status_code == 201
    created = json.loads(response.content.decode('utf8'))
    assert created.get('worker') == worker.get('id')
    assert created.get('agreement') == agreement.get('id')
    assert created.get('amount_rate') == amount_rate
    return created

def delete_worker_rate(worker_rate):
    response = requests.delete(endpoint_worker_rates, params={'id': worker_rate.get('id')})
    assert response.status_code == 200

