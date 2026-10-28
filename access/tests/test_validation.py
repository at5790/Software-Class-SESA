import pytest

from access.validation import OptimizationError, check_valid_campaign


def good(**changes):
    args = {"radius_km": 5, "max_sites": 2, "available_doses": 1000}
    args.update(changes)
    return args


def test_valid_campaign():
    assert check_valid_campaign(**good()) is True


def test_zero_radius_raises():
    with pytest.raises(ValueError):
        check_valid_campaign(**good(radius_km=0))


def test_text_radius_raises():
    # "5" has quotes, so it is text, not the number 5.
    # The radius must be a number, so the check raises OptimizationError.
    with pytest.raises(OptimizationError, match="radius_km"):
        check_valid_campaign(**good(radius_km="5"))


def test_negative_max_sites_raises():
    with pytest.raises(ValueError, match="max_sites"):
        check_valid_campaign(**good(max_sites=-1))


def test_negative_doses_raises():
    with pytest.raises(ValueError, match="available_doses"):
        check_valid_campaign(**good(available_doses=-5))


@pytest.mark.parametrize("field, value", [
    ("max_sites", 0),
    ("available_doses", 0),
])
def test_zero_is_allowed(field, value):
    assert check_valid_campaign(**good(**{field: value})) is True