# Distance-based route ordering for mobile vaccination units
import math


def distance(a, b):
    # finds direct distance between two coordinates
    return math.hypot(a[0] - b[0], a[1] - b[1])


def order_sites(start, sites):
    # Visit nearest unvisited site next
    # start: current coordinates of mobile unit, (x, y)
    # sites: dict of site names, with value (x, y)
    # Returns a list of site names in visiting order
    remaining = dict(sites)
    current = start
    route = []

    while remaining:
        # finding the site with min distance from current location
        nearest = None
        nearest_dist = None
        for name in remaining:
            d = distance(current, remaining[name])
            if nearest_dist is None or d < nearest_dist:
                nearest = name
                nearest_dist = d
        route.append(nearest)
        current = remaining.pop(nearest)

    return route
