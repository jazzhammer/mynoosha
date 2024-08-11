import json
from datetime import datetime, timedelta

from .test_clients import create_default_client, delete_client

import requests

from .test_invoices import create_invoice_for_client
from .test_work_types import get_work_type_for_name

endpoint_invoices = 'http://localhost:8001/api/v0/invoices/'
endpoint_invoice_items = 'http://localhost:8001/api/v0/invoice_items/'

TEST_DETAIL = "test detail"

def test_invoice_items():
    client = create_default_client()
    invoice = create_invoice_for_client(client)
    invoice_item = create_invoice_item_for_invoice(invoice)
    set_invoice_item_detail(invoice_item, TEST_DETAIL)
    work_type = get_work_type_for_name('milestone')
    set_invoice_item_work_type(invoice_item, work_type)

def set_invoice_item_work_type(invoice_item, work_type):
    response = requests.put(endpoint_invoice_items, data={
        'id': invoice_item.get('id'),
        'type': work_type.get('id')
    })
    assert response.status_code == 200
    updated = json.loads(response.content.decode('utf8'))
    assert updated.get('type') == work_type.get('id')

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