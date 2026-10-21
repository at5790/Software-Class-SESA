"""
Distances between GeoJSON points, in kilometers, and conversion to the
meters MongoDB's geo queries use.
"""
import math

from geo.points import to_lat_lon

# MongoDB's Earth radius, so distances here match its geo queries.
EARTH_RADIUS_KM = 6378.1

METERS_PER_KM = 1000


def haversine_km(lat1, lon1, lat2, lon2):
    """Great-circle distance in km between two latitude/longitude pairs."""
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = p2 - p1
    dl = math.radians(lon2 - lon1)
    a = (math.sin(dp / 2) ** 2
         + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2)
    return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(a))


def distance_km(point_a, point_b):
    """Distance in km between two GeoJSON points."""
    lat1, lon1 = to_lat_lon(point_a)
    lat2, lon2 = to_lat_lon(point_b)
    return haversine_km(lat1, lon1, lat2, lon2)


def km_to_meters(km):
    """Convert km to meters, the unit MongoDB's geo queries take."""
    return km * METERS_PER_KM
