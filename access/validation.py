"""Input checks for the access and optimization module."""


class OptimizationError(ValueError):
    """Bad campaign input; the API should answer 400."""


def is_number(val):
    return isinstance(val, (int, float)) and not isinstance(val, bool)


def is_whole(val):
    return isinstance(val, int) and not isinstance(val, bool)


def check_valid_campaign(radius_km, max_sites, available_doses):
    if not is_number(radius_km) or radius_km <= 0:
        raise OptimizationError("radius_km must be a number above 0.")
    if not is_whole(max_sites) or max_sites < 0:
        raise OptimizationError("max_sites must be a whole number >= 0.")
    if not is_whole(available_doses) or available_doses < 0:
        raise OptimizationError(
            "available_doses must be a whole number >= 0.")
    return True

