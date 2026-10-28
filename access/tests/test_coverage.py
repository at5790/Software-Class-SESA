from access.baseline import underserved_areas
from access.coverage import coverage_matrix


def test_matrix_covers_only_underserved_areas(areas, providers, candidates):
    under = underserved_areas(areas, providers, 5)
    assert coverage_matrix(candidates, under, 5) == {
        "c1": {"a4", "a5"},
        "c2": {"a5", "a6"},
        "c3": {"a7"},
        "c4": set(),
    }