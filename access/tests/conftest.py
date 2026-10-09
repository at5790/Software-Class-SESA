import pytest

from access import cache


def pt(lon, lat=0.0):
    """GeoJSON point. All fixture points sit on the equator,
    where 0.01 degrees of longitude is about 1.11 km."""
    return {"type": "Point", "coordinates": [lon, lat]}


@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()


@pytest.fixture
def areas():
    return [
        {"id": "a1", "population": 1000, "location": pt(0.00)},
        {"id": "a2", "population": 2000, "location": pt(0.02)},
        {"id": "a3", "population": 1500, "location": pt(0.04)},
        {"id": "a4", "population": 3000, "location": pt(0.10)},
        {"id": "a5", "population": 2500, "location": pt(0.13)},
        {"id": "a6", "population": 2000, "location": pt(0.17)},
        {"id": "a7", "population": 4000, "location": pt(0.40)},
    ]


@pytest.fixture
def providers():
    return [
        {"id": "p1", "active": True, "location": pt(0.01)},
        {"id": "p2", "active": False, "location": pt(0.40)},
        {"id": "p3", "active": True, "location": pt(0.80)},
    ]


@pytest.fixture
def candidates():
    return [
        {"id": "c1", "capacity": 3000, "location": pt(0.115)},
        {"id": "c2", "capacity": 3000, "location": pt(0.15)},
        {"id": "c3", "capacity": 500, "location": pt(0.40)},
        {"id": "c4", "capacity": 100, "location": pt(0.95)},
    ]


@pytest.fixture
def campaign():
    return {"id": "camp1", "radius_km": 5, "max_sites": 2,
            "available_doses": 10000}