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


def underserved_areas(areas, providers, radius_km):
    return [a for a in areas
            if not area_has_access(a, providers, radius_km)]


def baseline_coverage(areas, providers, radius_km):
    total = sum(a["population"] for a in areas)
    served = sum(a["population"] for a in areas
                 if area_has_access(a, providers, radius_km))
    return {
        "total_population": total,
        "covered_population": served,
        "coverage_pct": round(100 * served / total, 2) if total else 0.0,
    }
