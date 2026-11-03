def marginal_gain(reach_ids, covered_ids, pop_by_area):
    """Population newly reached: reach minus what is already covered."""
    return sum(pop_by_area[a] for a in reach_ids - covered_ids)