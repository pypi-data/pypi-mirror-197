from pypws.constants import *

def test_phast_client_id():
    assert PWS_CLIENT_ID == 'c02aee6b-4ab8-4fd8-9524-8bcd14617f1e'

def test_analytics_rest_api_uri():
    assert REST_API_URI == 'https://phastwebservices.dnv.com/api/'