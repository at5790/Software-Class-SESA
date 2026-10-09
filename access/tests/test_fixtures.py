def test_fixture_shapes(areas, providers, candidates, campaign):
    for a in areas:
        assert {"id", "population", "location"} <= a.keys()
    for p in providers:
        assert {"id", "active", "location"} <= p.keys()
    for c in candidates:
        assert {"id", "capacity", "location"} <= c.keys()
    assert campaign["max_sites"] == 2