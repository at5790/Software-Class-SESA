from http.client import (
    BAD_REQUEST,
    FORBIDDEN,
    NOT_ACCEPTABLE,
    NOT_FOUND,
    OK,
    SERVICE_UNAVAILABLE,
)

from unittest.mock import patch

from flask_restx import fields

import pytest

import server.endpoints as ep

TEST_CLIENT = ep.app.test_client()


def test_hello():
    resp = TEST_CLIENT.get(ep.HELLO_EP)
    resp_json = resp.get_json()
    assert ep.HELLO_RESP in resp_json


def test_endpoints():
    resp = TEST_CLIENT.get(ep.ENDPOINT_EP)
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert ep.ENDPOINT_RESP in resp_json
    # the list of routes should include our own routes
    assert ep.HELLO_EP in resp_json[ep.ENDPOINT_RESP]


TEST_STATES = {'Test State': {'capital': 'Test City'}}


# fake get_states so this only tests the endpoint itself
@patch('states.query.get_states', return_value=TEST_STATES)
def test_states(mock_get_states):
    resp = TEST_CLIENT.get(ep.STATES_EP)
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert resp_json[ep.STATE_RESP] == TEST_STATES
    mock_get_states.assert_called_once()

# tests Campaign for required fields 
def test_campaign_model_fields():
    expected = {
        'available_doses', 'mobile_units', 'max_sites',
        'radius', 'objective'
    }
    assert set(ep.campaign_model.keys()) == expected

def test_campaign_fields_required():
    for field in ep.campaign_model.values():
        assert field.required is True

def test_campaign_field_types():
    assert isinstance(ep.campaign_model['available_doses'], fields.Integer)
    assert isinstance(ep.campaign_model['radius'], fields.Float)
    assert isinstance(ep.campaign_model['objective'], fields.String)

def test_mobile_unit_model_fields():
    expected = {'name', 'dose_capacity', 'active', 'operating_window'}
    assert set(ep.mobile_unit_model.keys()) == expected

@pytest.mark.skip(reason='Endpoint for campaign creation not implemented')
def test_create_campaign():
    payload = {'available_doses': 100, 'mobile_units': 5, 'max_sites': 5,
               'radius': 100.0, 'objective': 'coverage'}
    response = TEST_CLIENT.post('/campaigns', json=payload)
    assert response.status_code == 201

def test_mobile_unit_fields_required():
    for field in ep.mobile_unit_model.values():
        assert field.required is True

def test_mobile_unit_field_types():
    assert isinstance(ep.mobile_unit_model['name'], fields.String)
    assert isinstance(ep.mobile_unit_model['dose_capacity'], fields.Integer)
    assert isinstance(ep.mobile_unit_model['active'], fields.Boolean)
    assert isinstance(ep.mobile_unit_model['operating_window'], fields.String)