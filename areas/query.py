"""
Queries for the areas collection.
"""
import data.db_connect as dbc

AREAS_COLLECTION = 'areas'
COUNTY_FIPS = 'county_fips'


def get_areas(county_fips, db=dbc.SE_DB):
    """Return every area in the county with this FIPS code."""
    return dbc.read(AREAS_COLLECTION, db=db, filt={COUNTY_FIPS: county_fips})
