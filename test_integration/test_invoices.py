import json
from datetime import datetime, timedelta

from .test_clients import create_default_client, delete_client

import requests

endpoint_invoices = 'http://localhost:8001/api/v0/invoices/'

def test_get():
    client = create_default_client()
    created = create_invoice_for_client(
        client
    )
    createds = get_invoices_for_client(client)
    assert len(createds) == 1
    created = createds[0]
    dt = datetime.fromisoformat(created['issued'])
    dt_10d = dt + timedelta(days=10)
    response = requests.put(endpoint_invoices, data={
        "id": created.get('id'),
        "issued": dt_10d.isoformat()
    })
    updated = json.loads(response.content.decode('utf8'))
    delete_invoices_for_client(client)
    delete_client(client)

def create_invoice_for_client(client):
    response = requests.post(endpoint_invoices, json={
        'client': client.get('id')
    })
    assert response.status_code == 201
    created = json.loads(response.content.decode('utf8'))
    assert created.get('client') == client.get('id')
    return created

def get_invoices_for_client(client):
    response = requests.get(endpoint_invoices, params={'client': client.get('id')})
    if response.status_code == 200:
        content = response.content.decode('utf8')
        founds = json.loads(content)
        return founds
    else:
        return None

def delete_invoices_for_client(client):
    founds = get_invoices_for_client(client)
    for found in founds:
        response = requests.delete(endpoint_invoices, params={'id': found['id']})
        assert response.status_code == 200
    founds = get_invoices_for_client(client)
    assert len(founds) == 0
