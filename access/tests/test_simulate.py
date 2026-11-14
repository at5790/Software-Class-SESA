import copy

from access.optimizer import simulate


def test_fewer_doses(campaign, areas, providers, candidates):
    result = simulate(campaign, areas, providers, candidates,
                      {"available_doses": 1000})
    sites = result["selected_sites"]
    assert [s["site_id"] for s in sites] == ["c1"]
    assert sites[0]["doses"] == 1000


def test_unavailable_site(campaign, areas, providers, candidates):
    result = simulate(campaign, areas, providers, candidates,
                      {"unavailable_site_ids": ["c1"]})
    assert [s["site_id"] for s in result["selected_sites"]] == ["c2", "c3"]
    assert result["metrics"]["post_coverage_pct"] == 81.25


def test_inputs_are_not_modified(campaign, areas, providers, candidates):
    before = copy.deepcopy((campaign, areas, providers, candidates))
    simulate(campaign, areas, providers, candidates, {"max_sites": 1})
    assert (campaign, areas, providers, candidates) == before