from route_planner import distance, order_sites


def test_distance():
    assert distance((0, 0), (3, 4)) == 5.0


def test_order_sites_nearest_first():
    sites = {"A": (1, 0), "B": (5, 0), "C": (2, 0)}
    assert order_sites((0, 0), sites) == ["A", "C", "B"]


def test_order_sites_empty():
    assert order_sites((0, 0), {}) == []

def test_distance_is_symmetric():
    assert distance((1, 2), (4, 6)) == distance((4, 6), (1, 2))


def test_distance_same_point_is_zero():
    assert distance((2, 2), (2, 2)) == 0.0


def test_distance_negative_coordinates():
    assert distance((-1, -1), (2, 3)) == 5.0

def test_tie_goes_to_first_listed_site():
    sites = {"A": (1, 0), "B": (-1, 0)}
    assert order_sites((0, 0), sites) == ["A", "B"]
