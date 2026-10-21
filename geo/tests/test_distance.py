import pytest

from geo.distance import distance_km, haversine_km, km_to_meters
from geo.points import make_point


def test_one_degree_of_longitude_at_equator():
    assert haversine_km(0, 0, 0, 1) == pytest.approx(111.32, abs=0.01)


def test_pole_to_pole():
    km = haversine_km(90, 0, -90, 0)
    assert km == pytest.approx(20037.39, abs=0.01)   # pi * 6378.1


def test_distance_km_reads_geojson_order():
    # At latitude 60, a degree of longitude is about half as long as at
    # the equator. Reading the coordinates in the wrong order would give
    # about 111 km instead.
    a, b = make_point(60, 0), make_point(60, 1)
    assert distance_km(a, b) == pytest.approx(55.66, abs=0.01)


def test_km_to_meters():
    assert km_to_meters(5) == 5000
