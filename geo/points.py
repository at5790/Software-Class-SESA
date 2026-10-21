"""
Building, reading and validating GeoJSON points.

GeoJSON stores coordinates as [lon, lat], the reverse of the (lat, lon)
order CSV files use. make_point() and to_lat_lon() are the only places
the order flips.
"""
import numbers

POINT = 'Point'

MIN_LAT, MAX_LAT = -90, 90
MIN_LON, MAX_LON = -180, 180


def make_point(lat, lon):
    """
    Return a GeoJSON point from a latitude and longitude, given in the
    order CSV files use. They can be numbers or numeric strings.
    Raises ValueError if they aren't valid coordinates.
    """
    try:
        lat, lon = float(lat), float(lon)
    except (TypeError, ValueError):
        raise ValueError('Coordinates must be numbers: '
                         f'lat={lat!r}, lon={lon!r}')
    point = {'type': POINT, 'coordinates': [lon, lat]}
    validate_point(point)
    return point


def to_lat_lon(point):
    """Return (lat, lon) from a GeoJSON point."""
    lon, lat = point['coordinates']
    return lat, lon


def validate_point(point):
    """
    Raise ValueError unless point is a GeoJSON point with two numeric
    coordinates, latitude from -90 to 90 and longitude from -180 to 180.
    """
    if not isinstance(point, dict) or point.get('type') != POINT:
        raise ValueError(f'Not a GeoJSON point: {point!r}')
    coords = point.get('coordinates')
    if not isinstance(coords, (list, tuple)) or len(coords) != 2:
        raise ValueError(f'Point coordinates must be [lon, lat]: {coords!r}')
    if not all(_is_number(c) for c in coords):
        raise ValueError(f'Coordinates must be numbers: {coords!r}')
    lon, lat = coords
    if not MIN_LAT <= lat <= MAX_LAT:
        raise ValueError(f'Latitude {lat} is outside {MIN_LAT} to {MAX_LAT}')
    if not MIN_LON <= lon <= MAX_LON:
        raise ValueError(f'Longitude {lon} is outside {MIN_LON} to {MAX_LON}')


def _is_number(value):
    # bool is a kind of int in Python, but True isn't a coordinate.
    return isinstance(value, numbers.Real) and not isinstance(value, bool)
