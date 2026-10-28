from access.geo import distance_km


def reachable_areas(candidate, areas_to_cover, radius_km):
    """Areas within radius_km of the candidate site."""
    return [
        a for a in areas_to_cover
        if distance_km(candidate["location"], a["location"]) <= radius_km
    ]


def coverage_matrix(candidates, areas_to_cover, radius_km):
    """candidate id -> set of area ids it can reach."""
    matrix = {}
    for c in candidates:
        reach = reachable_areas(c, areas_to_cover, radius_km)
        matrix[c["id"]] = {a["id"] for a in reach}
    return matrix