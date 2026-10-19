import pytest

from access.baseline import area_access, nearest_provider


def test_area_with_access(areas, providers):
    report = area_access(areas[0], providers, 5)
    assert report["has_access"] is True
    assert report["providers_in_range"] == ["p1"]


def test_underserved_area(areas, providers):
    report = area_access(areas[3], providers, 5)
    assert report["has_access"] is False
    assert report["providers_in_range"] == []


def test_nearest_provider(areas, providers):
    nearest = nearest_provider(areas[0], providers)
    assert nearest["provider_id"] == "p1"
    assert nearest["distance_km"] == pytest.approx(1.112, abs=0.01)


def test_nearest_ignores_inactive(areas, providers):
    assert nearest_provider(areas[6], providers)["provider_id"] == "p1"


def test_nearest_with_no_active_providers(areas):
    assert nearest_provider(areas[0], []) is None