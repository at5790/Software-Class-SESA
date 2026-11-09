from access.optimizer import allocate_doses

PICKS = [
    {"site_id": "c1", "new_area_ids": ["a4", "a5"], "gain": 5500},
    {"site_id": "c3", "new_area_ids": ["a7"], "gain": 4000},
    {"site_id": "c2", "new_area_ids": ["a6"], "gain": 2000},
]


def test_plenty_of_doses():
    allocated, left = allocate_doses(PICKS, 20000)
    assert [a["doses"] for a in allocated] == [5500, 4000, 2000]
    assert left == 8500


def test_runs_out_midway():
    allocated, left = allocate_doses(PICKS, 6000)
    assert [(a["site_id"], a["doses"]) for a in allocated] == [
        ("c1", 5500), ("c3", 500)]
    assert left == 0


def test_zero_doses_selects_nothing():
    assert allocate_doses(PICKS, 0) == ([], 0)