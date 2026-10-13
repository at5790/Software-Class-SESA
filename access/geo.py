import math

EARTH_RADIUS_KM = 6371.0088


def to_lat_lon(location):
    """GeoJSON point -> (lat, lon). GeoJSON order is [lon, lat]."""
    lon, lat = location["coordinates"]
    return lat, lon


def haversine_km(lat1, lon1, lat2, lon2):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = p2 - p1
    dl = math.radians(lon2 - lon1)
    a = (math.sin(dp / 2) ** 2
         + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2)
    return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(a))


def distance_km(loc_a, loc_b):
    lat1, lon1 = to_lat_lon(loc_a)
    lat2, lon2 = to_lat_lon(loc_b)
    return haversine_km(lat1, lon1, lat2, lon2)
