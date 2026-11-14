import pytest

from access.optimizer import optimize
from access.validation import OptimizationError


def test_no_candidates(campaign, areas, providers):
    result = optimize(campaign, areas, providers, [])
    assert result["selected_sites"] == []
    m = result["metrics"]
    assert m["post_coverage_pct"] == m["baseline_coverage_pct"]


def test_everyone_already_served(campaign, areas, providers, candidates):
    campaign["radius_km"] = 1000
    result = optimize(campaign, areas, providers, candidates)
    assert result["selected_sites"] == []
    assert result["metrics"]["baseline_coverage_pct"] == 100.0


def test_zero_doses(campaign, areas, providers, candidates):
    campaign["available_doses"] = 0
    result = optimize(campaign, areas, providers, candidates)
    assert result["selected_sites"] == []


def test_max_sites_larger_than_candidates(campaign, areas, providers,
                                          candidates):
    campaign["max_sites"] = 50
    sites = optimize(campaign, areas, providers, candidates)["selected_sites"]
    assert [s["site_id"] for s in sites] == ["c1", "c3", "c2"]


def test_missing_field_raises(campaign, areas, providers, candidates):
    del campaign["radius_km"]
    with pytest.raises(OptimizationError):
        optimize(campaign, areas, providers, candidates)


def test_negative_doses_raises(campaign, areas, providers, candidates):
    campaign["available_doses"] = -5
    with pytest.raises(OptimizationError):
        optimize(campaign, areas, providers, candidates)


def test_no_areas(campaign, providers, candidates):
    result = optimize(campaign, [], providers, candidates)
    assert result["metrics"]["post_coverage_pct"] == 0.0