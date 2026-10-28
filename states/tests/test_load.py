"""
Expected values come from the raw files themselves, so these tests check
the loader against its sources rather than against copied numbers.
"""
import csv

import pytest

import data.db_connect as dbc
import states.load as load
import states.query as qry


def read_rows(path, encoding='utf-8'):
    with open(path, newline='', encoding=encoding) as f:
        return list(csv.DictReader(f))


@pytest.fixture
def csv_rows():
    return read_rows(load.STATES_CSV)


def test_every_state_gets_its_census_fips(csv_rows):
    census = read_rows(load.CENSUS_STATES, encoding='utf-8-sig')
    census_fips = {row['STNAME']: row['STATEFP'] for row in census}
    docs = load.read_states()
    assert {d['name']: d['fips'] for d in docs} == {
        row['State']: census_fips[row['State']] for row in csv_rows}
    assert all(d[dbc.MONGO_ID] == d['fips'] for d in docs)


def test_location_is_the_csv_point(csv_rows):
    locations = {d['name']: d['location'] for d in load.read_states()}
    for row in csv_rows:
        lon, lat = locations[row['State']]['coordinates']
        assert (lat, lon) == (float(row['Latitude']), float(row['Longitude']))


def test_state_missing_from_census_stops_the_load(tmp_path, csv_rows):
    row = dict(csv_rows[0], State='Not a state')
    path = tmp_path / 'states.csv'
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=row)
        writer.writeheader()
        writer.writerow(row)
    with pytest.raises(ValueError, match='Bad row'):
        load.read_states(path)


def test_loading_again_replaces_the_states(loaded_states, csv_rows):
    load.load_states(db=dbc.TEST_DB)
    loaded = dbc.read(qry.STATES_COLLECTION, db=dbc.TEST_DB)
    assert len(loaded) == len(csv_rows)
