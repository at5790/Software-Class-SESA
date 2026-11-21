"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
# from http import HTTPStatus

from flask import Flask  # , request
from flask_restx import Resource, Api, fields  # Namespace
from flask_cors import CORS

# import werkzeug.exceptions as wz

import data.db_connect as dbc
import states.query as sqry

app = Flask(__name__)
CORS(app)
api = Api(app)

# Connect at startup, so the server log shows which MongoDB it uses.
dbc.connect_db()

campaign_model = api.model('Campaign', {
    'available_doses': fields.Integer
    (required=True, description="Available vaccine doses"),
    'mobile_units': fields.Integer
    (required=True, description="Number of mobile units"),
    'max_sites': fields.Integer
    (required=True, description="Maximum deployment sites"),
    'radius': fields.Float
    (required=True, description="Service radius"),
    'objective': fields.String
    (required=True, description="Optimization objective"),
})

mobile_unit_model = api.model('MobileUnit', {
    'name': fields.String(
        required=True, description="Mobile unit name"),
    "dose_capacity": fields.Integer(
        required=True, description="Maximum vaccine doses"),
    'active': fields.Boolean(
        required=True, description="Whether unit is active"),
    'operating_window': fields.String(
        required=True, description="Operating schedule"),
})


def validate_campaign(data):
    for field in ("available_doses", "mobile_units", "max_sites"):
        if data.get(field, 0) < 0:
            return f'{field} cannot be negative'
    if data.get("radius", 0) <= 0:
        return "radius must be positive"
    return None


def validate_mobile_unit(data):
    if not data.get("name"):
        return "Mobile unit name is required"
    if data.get("dose_capacity", 0) <= 0:
        return "Dose capacity must be positive"
    if not data.get("operating_window"):
        return "Operating window is required"
    return None


ENDPOINT_EP = '/endpoints'
ENDPOINT_RESP = 'Available endpoints'
HELLO_EP = '/hello'
HELLO_RESP = 'hello'
STATES_EP = '/states'
STATE_RESP = 'States:'
MESSAGE = 'Message'


@api.route(HELLO_EP)
class HelloWorld(Resource):
    """
    The purpose of the HelloWorld class is to have a simple test to see if the
    app is working at all.
    """
    def get(self):
        """
        A trivial endpoint to see if the server is running.
        """
        return {HELLO_RESP: 'world'}


@api.route(ENDPOINT_EP)
class Endpoints(Resource):
    """
    This class will serve as live, fetchable documentation of what endpoints
    are available in the system.
    """
    def get(self):
        """
        The `get()` method will return a sorted list of available endpoints.
        """
        endpoints = sorted(rule.rule for rule in api.app.url_map.iter_rules())
        return {"Available endpoints": endpoints}


@api.route(STATES_EP)
class States(Resource):
    """
    The get method will return a list of all states in the database.
    """
    def get(self):
        """
        The get method will return a list of all states in the database.
        """
        states = sqry.get_states()
        return {STATE_RESP: states}
