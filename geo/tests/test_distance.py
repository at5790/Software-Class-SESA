"""
Distances must agree with MongoDB, because some coverage checks run in
Python and some run as MongoDB radius queries. So these tests compare
geo.distance with MongoDB's own distances.
"""
import pytest

import data.db_connect as dbc
from geo.distance import distance_km, km_to_meters
from geo.points import make_point

COLLECTION = 'geo_distance_tests'

# NYU Tandon, Brooklyn, NY.
ORIGIN = make_point(40.6943708, -73.9865765)

# Points near and far, north and south, east and west of the origin.
POINTS = [make_point(lat, lon)
          for lat in (-60, 0, 40.7, 60, 89)
          for lon in (-179, -74, -73.98, 0, 100)]


@pytest.fixture
def mongo_meters():
    """MongoDB's distance in meters from ORIGIN to each of POINTS."""
    coll = dbc.get_collection(COLLECTION, db=dbc.TEST_DB)
    coll.drop()
    coll.insert_many([{'i': i, 'location': p} for i, p in enumerate(POINTS)])
    coll.create_index([('location', '2dsphere')])
    rows = coll.aggregate([{'$geoNear': {
        'near': ORIGIN, 'distanceField': 'meters', 'spherical': True}}])
    meters = {row['i']: row['meters'] for row in rows}
    yield [meters[i] for i in range(len(POINTS))]
    coll.drop()


def test_distances_match_mongodb(mongo_meters):
    python_meters = [km_to_meters(distance_km(ORIGIN, p)) for p in POINTS]
    assert python_meters == pytest.approx(mongo_meters)
