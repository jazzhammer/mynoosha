import json
import requests

from test_integration.utils.time_utils import utc_dt, utc_ts

endpoint_clients = 'http://localhost:8001/api/v0/clients/'
endpoint_work_intervals = 'http://localhost:8001/api/v0/work_intervals/'
endpoint_utc = 'http://localhost:8001/api/v0/utc/'
TEST_NAME = 'busyclient'



def test_crud():
    client = confirmClientExists(TEST_NAME)
    deleteClientWorkIntervalsByClientId(client.get('id'))
    createds = createClientWorkIntervals(client, 3, -1)
    assert len(createds) == 3
    created = createds[0]
    updated = updateWorkIntervalStop(created)
    updated = updateWorkIntervalDescription(updated)
    deleteWorkIntervalById(updated.get('id'))
    deleteClientWorkIntervalsByClientId(client.get('id'))
    createds = createClientWorkIntervals(client, 3, -1)
    assert len(createds) == 3
    reads = readClientWorkIntervals(client=client, hour_offset=-2)
    assert len(reads) == 3
    deleteClientWorkIntervalsByClientId(client.get('id'))
    # ============================================================
    # cRud, with getting by datetime boundaries
    # ============================================================
    created = createClientWorkInterval(client)
    founds = readWorkIntervals(hours_offset=-2)
    assert len([instance for instance in founds if instance['id'] == created['id']]) > 0
    founds = readWorkIntervals(hours_offset=2)
    assert len([instance for instance in founds if instance['id'] == created['id']]) == 0
    # ============================================================
    # updates & creates, relative to existing WorkIntervals' starts
    # ============================================================
    deleteClientWorkIntervalsByClientId(client.get('id'))
    # earlier creation really should be earlier
    # create the later one first
    later = createClientWorkInterval(client, description='later')
    earlier = createClientWorkInterval(client, hours_offset=-1, description='earlier')
    assert earlier.get('start_utcms') < later.get('start_utcms')
    # creating with earlier start than another start must result in:
    # the earlier created.stop set to the other's start
    # the earlier would have been mutated by this exercise, so re-read:
    earlier = readWorkIntervals(id=earlier.get('id'))[0]
    assert later.get('start_utcms') == earlier.get('stop_utcms')

    # earlier creation really should be earlier
    # create the later one first
    deleteClientWorkIntervalsByClientId(client.get('id'))
    later = createClientWorkInterval(client, description='later')
    earlier = createClientWorkInterval(client, hours_offset=-1, description='earlier')
    assert earlier.get('start_utcms') < later.get('start_utcms')
    # creating with earlier start than another start must result in:
    # the earlier created.stop set to the other's start
    # the earlier would have been mutated by this exercise, so re-read:
    earlier = readWorkIntervals(id=earlier.get('id'))[0]
    assert later.get('start_utcms') == earlier.get('stop_utcms')
    set_work_interval_invoice_item(later, 1)

    # get_invoiceable_work_intervals_for_client(client)

def set_work_interval_invoice_item(work_interval, invoice_item):
    response = requests.put(endpoint_work_intervals, data={
        'id': work_interval.get('id'),
        'invoice_item': invoice_item
    })
    assert response.status_code == 200
    updated = json.loads(response.content.decode('utf8'))
    assert updated.get('invoice_item') == invoice_item

def get_invoiceable_work_intervals_for_client(client):
    requests.get(endpoint_work_intervals, params={
        'client': client.id,
        'invoice_item': 1
    })

def deleteClientWorkIntervalsByClientId(client_id):
    intervals_response = requests.get(endpoint_work_intervals, params={'client': client_id})
    if intervals_response.status_code == 200:
        founds = json.loads(intervals_response.content.decode('utf8'))
        for found in founds:
            requests.delete(endpoint_work_intervals, params={'id': found['id']})
    response = requests.get(endpoint_work_intervals, params={'client': client_id})
    assert response.status_code >= 200


# hours_offset negative => in the past
# hours_offset positive => in the future
# relative to now()
def createClientWorkIntervals(client, qty, hours_offset):
    print(f"createClientWorkIntervals({client=},{qty=})")
    createds = []
    for w in range(qty):
        created = createClientWorkInterval(client, hours_offset)
        createds.append(created)
    print(f"created WorkIntervals({len(createds)=}) for Client[{client['id']=}]")
    return createds


# hours_offset negative => in the past
# hours_offset positive => in the future
# relative to now()
def createClientWorkInterval(client, *args, **kwargs):
    hours_offset = kwargs.get('hours_offset')
    dt_str = str(utc_dt(hours_offset=hours_offset))
    description = 'a test interval'
    if kwargs.get('description'):
        description = kwargs.get('description')
    post_parms = {
        'start': dt_str,
        'client': client['id'],
        'description': description
    }
    response = requests.post(endpoint_work_intervals, json=post_parms)
    created = json.loads(response.content.decode('utf8'))
    assert created
    assert response.status_code == 201
    print(f"created WorkInterval({client=},{hours_offset=})")
    return created


def readClientWorkIntervals(*args, **kwargs):
    client = kwargs.get('client')
    hours_offset = kwargs.get('hours_offset')
    params = {}
    if client:
        params['client'] = client.get('id')
    if hours_offset:
        params['pre_start'] = utc_dt(hours_offset=hours_offset)
    response = requests.get(endpoint_work_intervals, params=params)
    founds = json.loads(response.content.decode('utf8'))
    return founds


def updateWorkIntervalStop(interval):
    next_stop = str(utc_dt())
    interval['stop'] = next_stop
    edited = interval
    response = requests.put(endpoint_work_intervals, json=edited)
    assert response.status_code == 200
    updated = json.loads(response.content.decode('utf8'))
    assert updated['stop'] == next_stop
    response = requests.get(endpoint_utc, params={'iso_format': next_stop})
    expected_stop = float(response.content.decode('utf8'))
    assert updated.get('stop_utcms') == round(expected_stop)
    return updated


def updateWorkIntervalDescription(interval):
    old_description = interval.get('description')
    next_description = f"next_description"
    interval['description'] = next_description
    edited = interval
    response = requests.put(endpoint_work_intervals, json=edited)
    assert response.status_code == 200
    updated = json.loads(response.content.decode('utf8'))
    assert updated['description'] == next_description
    return updated


def deleteWorkIntervalById(interval_id):
    response = requests.delete(endpoint_work_intervals, params={'id': interval_id})
    assert response.status_code == 200
    response = requests.get(endpoint_work_intervals, params={'id': interval_id})
    assert response.status_code >= 200


def confirmClientExists(name):
    response = requests.get(endpoint_clients, params={'search': name})
    if response.status_code != 200:
        response = requests.post(endpoint_clients, json={'name': name})
        assert response.status_code == 201
        found = json.loads(response.content.decode('utf8'))
    else:
        founds = json.loads(response.content.decode('utf8', errors='strict'))
        found = founds[0]
    return found


def readWorkIntervals(*args, **kwargs):
    hours_offset = kwargs.get('hours_offset')
    params = {}
    if kwargs.get('hours_offset'):
        ago_delta = utc_dt(hours_offset=hours_offset)
        params = {'pre_start': str(ago_delta)}
    if kwargs.get('id'):
        params['id'] = kwargs.get('id')

    response = requests.get(endpoint_work_intervals, params=params)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf8'))
    else:
        return []
