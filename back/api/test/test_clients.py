import requests

endpoint_get = 'http://localhost:8001/api/v0/clients/'
def test_get():
    requests.get(endpoint_get, params={})