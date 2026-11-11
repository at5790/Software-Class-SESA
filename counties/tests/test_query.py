from collections import defaultdict

import counties.load as load
import counties.query as qry
import data.db_connect as dbc


def test_get_counties_returns_each_states_counties(loaded_counties):
    expected = defaultdict(dict)
    for county in load.read_counties():
        del county[dbc.MONGO_ID]
        expected[county['state_fips']][county['fips']] = county
    for state_fips, counties in expected.items():
        found = qry.get_counties(state_fips, db=dbc.TEST_DB)
        assert {c['fips']: c for c in found} == counties
