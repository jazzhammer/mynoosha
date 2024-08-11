import json
from datetime import datetime, timedelta

from .test_clients import create_default_client, delete_client

import requests

from .test_invoices import create_invoice_for_client
from .test_work_intervals import createClientWorkInterval
from .test_work_types import get_work_type_for_name

endpoint_invoices = 'http://localhost:8001/api/v0/invoices/'
endpoint_invoice_items = 'http://localhost:8001/api/v0/invoice_items/'

TEST_DETAIL_0 = "test detail 0"
TEST_DETAIL_1 = "test detail 1"
def test_invoice_items():
    client = create_default_client()
    # setup for create
    invoice = create_invoice_for_client(client)
    work_type = get_work_type_for_name('milestone')
    work_interval = createClientWorkInterval(client)

    # create with partial and fullset of foreign keys : invoice, work_interval, work_type
    response = requests.post(endpoint_invoice_items, data={
        'invoice': invoice.get('id'),
        'work_interval': work_interval.get('id'),
        'work_type': work_type.get('id')
    })
    assert response.status_code == 201
    created = json.loads(response.content.decode('utf8'))
    assert created.get('invoice') == invoice.get('id')
    assert created.get('work_type') == work_type.get('id')

    work_type = get_work_type_for_name('time')
    set_invoice_item_detail(created, TEST_DETAIL_0)
    set_invoice_item_work_type(created, work_type)


def set_invoice_item_work_type(invoice_item, work_type):
    response = requests.put(endpoint_invoice_items, data={
        'id': invoice_item.get('id'),
        'work_type': work_type.get('id')
    })
    assert response.status_code == 200
    updated = json.loads(response.content.decode('utf8'))
    assert updated.get('work_type') == work_type.get('id')

def create_invoice_item_for_invoice(invoice):
    response = requests.post(endpoint_invoice_items, data={
        'invoice': invoice.get('id')
    })
    assert response.status_code == 201
    return json.loads(response.content.decode('utf8'))

def set_invoice_item_detail(invoice_item, detail):
    response = requests.put(endpoint_invoice_items, data={
        'id': invoice_item.get('id'),
        'detail': detail
    })
    assert response.status_code == 200
    updated = json.loads(response.content.decode('utf8'))
    assert updated.get('detail') == detail