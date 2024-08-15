import json
from datetime import datetime, timezone
import requests

from test_integration.test_clients import create_default_client, create_client_for_name, delete_client
from test_integration.test_invoice_items import create_invoice_item, delete_invoice_item
from test_integration.test_invoices import delete_invoice
from test_integration.test_work_intervals import delete_work_interval

endpoint_work_pieces = 'http://localhost:8001/api/v0/work_pieces/'
TEST_NAME = 'testingONLYname'
TEST_DESCRIPTION = 'testONLYDescription'


def test_get():
    start = datetime.now(timezone.utc)
    client = create_default_client()
    created = create_work_piece(
        TEST_NAME,
        TEST_DESCRIPTION,
        start,
        client
    )
    update_name(created, 'new test name')
    update_description(created, 'new test description')
    next_client = create_client_for_name('next client')
    update_client(created, next_client)
    invoice_item_details = create_invoice_item()
    next_invoice_item = invoice_item_details.get('invoice_item')
    update_invoice_item(created, next_invoice_item)
    # deleteWorkPiecesForName(created.get('name'))
    # founds = getWorkPiecesForName(TEST_NAME)
    # assert founds == []
    # founds = get_all_work_pieces()
    deleted = delete_work_piece(created)
    deleted = delete_client(next_client)
    deleted = delete_client(client)

    deleted = delete_work_interval(invoice_item_details.get('work_interval'))
    deleted = delete_invoice_item(invoice_item_details.get('invoice_item'))
    deleted = delete_invoice(invoice_item_details.get('invoice'))


def update_invoice_item(work_piece, next_invoice_item):
    work_piece['invoice_item'] = next_invoice_item.get('id')
    response = requests.put(endpoint_work_pieces, data={**work_piece})
    assert response.status_code == 200
    updated = json.loads(response.content.decode('utf8'))
    assert updated.get('invoice_item') == next_invoice_item.get('id')

def update_client(work_piece, next_client):
    work_piece['client'] = next_client.get('id')
    response = requests.put(endpoint_work_pieces, data={**work_piece})
    assert response.status_code == 200
    updated = json.loads(response.content.decode('utf8'))
    assert updated.get('client') == next_client.get('id')

def update_name(work_piece, next_name):
    work_piece['name'] = next_name
    response = requests.put(endpoint_work_pieces, data={**work_piece})
    assert response.status_code == 200
    updated = json.loads(response.content.decode('utf8'))
    assert updated.get('name') == next_name


def update_description(work_piece, next_description):
    work_piece['description'] = next_description
    response = requests.put(endpoint_work_pieces, data={**work_piece})
    assert response.status_code == 200
    updated = json.loads(response.content.decode('utf8'))
    assert updated.get('description') == next_description


def get_all_work_pieces():
    response = requests.get(endpoint_work_pieces, params={})
    assert response.status_code == 200
    founds = json.loads(response.content.decode('utf8'))
    assert len(founds) == 3

def create_work_piece(
        name,
        test_description,
        start: datetime,
        client
    ):
    response = requests.post(endpoint_work_pieces, json={
        'name': name,
        'description': test_description,
        'start': start.isoformat(),
        'client': client.get('id')
    })
    assert response.status_code == 201

    created = json.loads(response.content.decode('utf8'))
    assert created.get('name') == name
    assert created.get('description') == test_description
    return created

def get_work_piece_for_name(name):
    response = requests.get(endpoint_work_pieces, params={'name': name})
    if response.status_code == 200:
        content = response.content.decode('utf8')
        found = json.loads(content)[0]
        return found
    else:
        return None

def getWorkPiecesForName(name):
    response = requests.get(endpoint_work_pieces, params={'search': name})
    if response.status_code == 200:
        content = response.content.decode('utf8')
        founds = json.loads(content)
        return founds
    else:
        return None

def deleteWorkPiecesForName(name):
    founds = getWorkPiecesForName(name)
    for found in founds:
        response = requests.delete(endpoint_work_pieces, params={'id': found['id']})
        assert response.status_code == 200
    response = requests.get(endpoint_work_pieces, params={'search': name})
    assert response.status_code == 200

def delete_work_piece(work_piece):
    response = requests.delete(endpoint_work_pieces, params={'id': work_piece.get('id')})
    assert response.status_code == 200
