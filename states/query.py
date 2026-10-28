"""
Queries for the states collection.
"""
import data.db_connect as dbc

STATES_COLLECTION = 'states'
CODE = 'code'


def get_states(db=dbc.SE_DB):
    """Return every state, keyed by its two-letter code."""
    return dbc.read_dict(STATES_COLLECTION, CODE, db=db)
