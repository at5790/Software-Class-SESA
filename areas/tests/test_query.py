from collections import defaultdict

import areas.load as load
import areas.query as qry
import data.db_connect as dbc


def test_get_areas_returns_each_countys_areas(loaded_areas):
    expected = defaultdict(dict)
    for area in load.read_areas():
        del area[dbc.MONGO_ID]
        expected[area['county_fips']][area['geoid']] = area
    for county_fips, areas in expected.items():
        found = qry.get_areas(county_fips, db=dbc.TEST_DB)
        assert {a['geoid']: a for a in found} == areas
