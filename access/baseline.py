from access.geo import distance_km


def providers_in_range(location, providers, radius_km):
    """Ids of ACTIVE providers within radius_km of a location."""
    return [
        p["id"] for p in providers
        if p.get("active", True)
        and distance_km(location, p["location"]) <= radius_km
    ]


def area_has_access(area, providers, radius_km):
    nearby = providers_in_range(area["location"], providers, radius_km)
    return len(nearby) > 0
