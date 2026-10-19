import pytest

from access.baseline import area_has_access, baseline_coverage
from access.baseline import underserved_areas
from access.geo import distance_km


def test_underserved_ids(areas, providers):
    ids = [a["id"] for a in underserved_areas(areas, providers, 5)]
    assert ids == ["a4", "a5", "a6", "a7"]


def test_baseline_coverage(areas, providers):
    result = baseline_coverage(areas, providers, 5)
    assert result["total_population"] == 16000
    assert result["covered_population"] == 4500
    assert result["coverage_pct"] == pytest.approx(28.125, abs=0.01)


def test_no_areas_gives_zero_not_crash(providers):
    assert baseline_coverage([], providers, 5)["coverage_pct"] == 0.0


def test_radius_boundary_is_inclusive(areas, providers):
    d = distance_km(areas[0]["location"], providers[0]["location"])
    assert area_has_access(areas[0], providers[:1], d)