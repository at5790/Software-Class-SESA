"""
Expected values come from the Census files themselves, so these tests check
the loader against its sources rather than against copied numbers.
"""
import csv

import pytest

import counties.load as load
import counties.query as qry
import data.db_connect as dbc
import states.load as states_load


@pytest.fixture
def census_rows():
    with open(load.CENSUS_COUNTIES, newline='', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))


def test_every_census_county_is_loaded(census_rows):
    counties = {c['fips']: c for c in load.read_counties()}
    assert len(counties) == len(census_rows)
    for row in census_rows:
        county = counties[row['STATEFP'] + row['COUNTYFP']]
        assert county[dbc.MONGO_ID] == county['fips']
        assert county['name'] == row['COUNAME']
        assert county['state_fips'] == row['STATEFP']
        assert county['population'] == int(row['POPULATION'])
        lon, lat = county['location']['coordinates']
        assert (lat, lon) == (float(row['LATITUDE']), float(row['LONGITUDE']))


def test_every_county_belongs_to_a_loaded_state():
    state_fips = {s['fips'] for s in states_load.read_states()}
    assert {c['state_fips'] for c in load.read_counties()} <= state_fips


def test_loading_again_replaces_the_counties(loaded_counties, census_rows):
    load.load_counties(db=dbc.TEST_DB)
    loaded = dbc.read(qry.COUNTIES_COLLECTION, db=dbc.TEST_DB)
    assert len(loaded) == len(census_rows)
