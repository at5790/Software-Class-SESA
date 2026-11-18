"""
Expected values come from the Census files themselves, so these tests check
the loader against its sources rather than against copied numbers.
"""
import csv
from collections import defaultdict

import pytest

import areas.load as load
import areas.query as qry
import counties.load as counties_load
import data.db_connect as dbc


@pytest.fixture
def tract_rows():
    rows = []
    for path in load.TRACT_FILES:
        with open(path, newline='', encoding='utf-8-sig') as f:
            rows.extend(csv.DictReader(f))
    return rows


def test_every_tract_becomes_an_area(tract_rows):
    areas = {a['geoid']: a for a in load.read_areas()}
    assert len(areas) == len(tract_rows)
    for row in tract_rows:
        county_fips = row['STATEFP'] + row['COUNTYFP']
        area = areas[county_fips + row['TRACTCE']]
        assert area[dbc.MONGO_ID] == area['geoid']
        assert area['state_fips'] == row['STATEFP']
        assert area['county_fips'] == county_fips
        assert area['population'] == int(row['POPULATION'])
        assert area['target_population'] == area['population']
        lon, lat = area['location']['coordinates']
        assert (lat, lon) == (float(row['LATITUDE']), float(row['LONGITUDE']))


def test_tract_populations_add_up_to_their_county():
    county_population = {c['fips']: c['population']
                         for c in counties_load.read_counties()}
    totals = defaultdict(int)
    for area in load.read_areas():
        totals[area['county_fips']] += area['population']
    assert totals == {fips: county_population[fips] for fips in totals}


def test_loading_again_replaces_the_areas(loaded_areas, tract_rows):
    load.load_areas(db=dbc.TEST_DB)
    loaded = dbc.read(qry.AREAS_COLLECTION, db=dbc.TEST_DB)
    assert len(loaded) == len(tract_rows)
