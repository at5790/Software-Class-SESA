import pytest

from access.baseline import underserved_areas
from access.coverage import coverage_matrix
from access.optimizer import select_sites


@pytest.fixture
def matrix_and_pop(areas, providers, candidates):
    under = underserved_areas(areas, providers, 5)
    matrix = coverage_matrix(candidates, under, 5)
    return matrix, {a["id"]: a["population"] for a in under}


def test_picks_best_then_recomputes(matrix_and_pop):
    matrix, pop = matrix_and_pop
    picks = select_sites(matrix, pop, 2)
    assert [p["site_id"] for p in picks] == ["c1", "c3"]
    assert [p["gain"] for p in picks] == [5500, 4000]


def test_overlap_is_not_double_counted(matrix_and_pop):
    matrix, pop = matrix_and_pop
    picks = select_sites(matrix, pop, 3)
    assert [p["site_id"] for p in picks] == ["c1", "c3", "c2"]
    assert picks[2]["new_area_ids"] == ["a6"]    # a5 already belonged to c1


def test_zero_gain_site_never_picked(matrix_and_pop):
    matrix, pop = matrix_and_pop
    ids = [p["site_id"] for p in select_sites(matrix, pop, 10)]
    assert "c4" not in ids


def test_max_sites_zero(matrix_and_pop):
    matrix, pop = matrix_and_pop
    assert select_sites(matrix, pop, 0) == []


def test_ties_go_to_lowest_id():
    matrix = {"b": {"x"}, "a": {"y"}}
    picks = select_sites(matrix, {"x": 10, "y": 10}, 1)
    assert picks[0]["site_id"] == "a"