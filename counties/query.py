"""
Queries for the counties collection.
"""
import data.db_connect as dbc

COUNTIES_COLLECTION = 'counties'
STATE_FIPS = 'state_fips'


def get_counties(state_fips, db=dbc.SE_DB):
    """Return every county in the state with this FIPS code."""
    return dbc.read(COUNTIES_COLLECTION, db=db, filt={STATE_FIPS: state_fips})
