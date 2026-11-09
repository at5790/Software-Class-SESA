def marginal_gain(reach_ids, covered_ids, pop_by_area):
    """Population newly reached: reach minus what is already covered."""
    return sum(pop_by_area[a] for a in reach_ids - covered_ids)


def select_sites(matrix, pop_by_area, max_sites):
    """Greedy max coverage. Returns picks in selection order."""
    covered = set()
    remaining = dict(matrix)
    picks = []
    while remaining and len(picks) < max_sites:
        scored = [
            (-marginal_gain(ids, covered, pop_by_area), cid)
            for cid, ids in remaining.items()
        ]
        best_id = min(scored)[1]         
        new_ids = remaining.pop(best_id) - covered
        gain = sum(pop_by_area[a] for a in new_ids)
        if gain <= 0:
            break
        picks.append({"site_id": best_id,
                      "new_area_ids": sorted(new_ids),
                      "gain": gain})
        covered |= new_ids
    return picks


def allocate_doses(picks, available_doses, capacity_by_site=None):
    """Each pick gets min(gain, capacity, doses left)."""
    capacity_by_site = capacity_by_site or {}
    left = available_doses
    allocated = []
    for p in picks:
        cap = capacity_by_site.get(p["site_id"], p["gain"])
        doses = min(p["gain"], cap, left)
        if doses <= 0:
            continue
        allocated.append(dict(p, doses=doses))
        left -= doses
    return allocated, left