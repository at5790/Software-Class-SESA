import pytest

from geo.points import make_point, to_lat_lon, validate_point

# NYU Tandon, Brooklyn, NY.
LAT, LON = 40.6943708, -73.9865765


def test_make_point_puts_longitude_first():
    point = make_point(LAT, LON)
    assert point == {'type': 'Point', 'coordinates': [LON, LAT]}


def test_make_point_accepts_csv_strings():
    assert make_point('40.6943708', '-73.9865765') == make_point(LAT, LON)


@pytest.mark.parametrize('lat', ['', None])
def test_make_point_rejects_non_numbers(lat):
    with pytest.raises(ValueError):
        make_point(lat, LON)


def test_make_point_rejects_out_of_range():
    with pytest.raises(ValueError):
        make_point(91, LON)


def test_to_lat_lon_undoes_make_point():
    assert to_lat_lon(make_point(LAT, LON)) == (LAT, LON)


@pytest.mark.parametrize('coords', [
    [LON, LAT],
    [0, 0],
    [180, 90],      # the edges are allowed
    [-180, -90],
])
def test_validate_point_accepts_valid_points(coords):
    validate_point({'type': 'Point', 'coordinates': coords})


@pytest.mark.parametrize('point', [
    None,
    {'coordinates': [LON, LAT]},
    {'type': 'Point'},
    {'type': 'Point', 'coordinates': [LON, LAT, 0]},
    {'type': 'Point', 'coordinates': ['-73.9865765', '40.6943708']},
    {'type': 'Point', 'coordinates': [True, False]},
    {'type': 'Point', 'coordinates': [0, 90.5]},
    {'type': 'Point', 'coordinates': [-180.5, 0]},
    {'type': 'Point', 'coordinates': [0, float('nan')]},
])
def test_validate_point_rejects_invalid_points(point):
    with pytest.raises(ValueError):
        validate_point(point)
