from access.optimizer import optimize


def test_example_scenario(campaign, areas, providers, candidates):
    result = optimize(campaign, areas, providers, candidates)
    sites = result["selected_sites"]
    assert [s["site_id"] for s in sites] == ["c1", "c3"]
    assert [s["doses"] for s in sites] == [3000, 500]
    assert result["metrics"]["post_coverage_pct"] == 87.5
    assert result["metrics"]["additional_population"] == 9500


def test_no_double_counting(campaign, areas, providers, candidates):
    campaign["max_sites"] = 3
    sites = optimize(campaign, areas, providers, candidates)["selected_sites"]
    by_id = {s["site_id"]: s for s in sites}
    assert by_id["c2"]["new_area_ids"] == ["a6"]
    assert by_id["c2"]["doses"] == 2000