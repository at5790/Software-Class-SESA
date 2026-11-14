import pytest

from access.optimizer import impact_metrics

BASELINE = {"total_population": 16000, "covered_population": 4500,
            "coverage_pct": 28.12}


def test_two_sites():
    allocated = [{"gain": 5500, "doses": 3000}, {"gain": 4000, "doses": 500}]
    m = impact_metrics(BASELINE, allocated, 10000, 6500)
    assert m["post_coverage_pct"] == 87.5
    assert m["additional_population"] == 9500
    assert m["doses_allocated"] == 3500
    assert m["sites_selected"] == 2


def test_no_sites_equals_baseline():
    m = impact_metrics(BASELINE, [], 0, 0)
    assert m["post_coverage_pct"] == pytest.approx(28.12, abs=0.01)
    assert m["additional_population"] == 0