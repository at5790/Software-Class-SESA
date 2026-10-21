import pytest

from access.geo import distance_km, haversine_km


def test_same_point_is_zero():
    assert haversine_km(40.0, -74.0, 40.0, -74.0) == 0


def test_one_degree_of_longitude_at_equator():
    assert haversine_km(0, 0, 0, 1) == pytest.approx(111.32, abs=0.1)


def test_known_city_pair():
    d = haversine_km(40.7128, -74.0060, 34.0522, -118.2437)
    assert d == pytest.approx(3936, abs=20)


def test_symmetric():
    assert haversine_km(10, 20, 30, 40) == pytest.approx(
        haversine_km(30, 40, 10, 20))


def test_distance_km_reads_geojson_order():
    p1 = {"type": "Point", "coordinates": [0, 0]}
    p2 = {"type": "Point", "coordinates": [1, 0]}
    assert distance_km(p1, p2) == pytest.approx(111.32, abs=0.1)
