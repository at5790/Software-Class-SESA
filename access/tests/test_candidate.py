from access.baseline import underserved_areas
from access.coverage import candidate_coverage


def test_candidate_report(areas, providers, candidates):
    under = underserved_areas(areas, providers, 5)
    report = candidate_coverage(candidates[0], under, 5)
    assert report["area_ids"] == ["a4", "a5"]
    assert report["reachable_population"] == 5500


def test_candidate_reaching_nothing(areas, providers, candidates):
    under = underserved_areas(areas, providers, 5)
    report = candidate_coverage(candidates[3], under, 5)
    assert report["area_ids"] == []
    assert report["reachable_population"] == 0