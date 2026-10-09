from route_planner import distance, order_sites


def test_distance():
    assert distance((0, 0), (3, 4)) == 5.0


def test_order_sites_nearest_first():
    sites = {"A": (1, 0), "B": (5, 0), "C": (2, 0)}
    assert order_sites((0, 0), sites) == ["A", "C", "B"]


def test_order_sites_empty():
    assert order_sites((0, 0), {}) == []
