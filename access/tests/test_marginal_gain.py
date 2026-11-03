from access.optimizer import marginal_gain

POP = {"a4": 3000, "a5": 2500, "a6": 2000}


def test_nothing_covered_yet():
    assert marginal_gain({"a4", "a5"}, set(), POP) == 5500


def test_overlap_not_double_counted():
    assert marginal_gain({"a5", "a6"}, {"a4", "a5"}, POP) == 2000


def test_fully_covered_gives_zero():
    assert marginal_gain({"a4"}, {"a4", "a5"}, POP) == 0