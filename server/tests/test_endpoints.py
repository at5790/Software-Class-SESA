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


def test_states():
    resp = TEST_CLIENT.get(ep.STATES_EP)
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert ep.STATE_RESP in resp_json
    assert isinstance(resp_json[ep.STATE_RESP], dict)

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
