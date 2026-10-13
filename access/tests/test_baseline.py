from access.baseline import area_has_access, providers_in_range


def test_active_provider_in_range(areas, providers):
    assert providers_in_range(areas[0]["location"], providers, 5) == ["p1"]


def test_inactive_provider_is_ignored(areas, providers):
    a7 = areas[6]   # sits exactly on inactive provider p2
    assert providers_in_range(a7["location"], providers, 5) == []


def test_area_has_access(areas, providers):
    assert area_has_access(areas[2], providers, 5)       # a3, 3.3 km
    assert not area_has_access(areas[2], providers, 3)   # radius too small
    assert not area_has_access(areas[3], providers, 5)   # a4, 10 km
