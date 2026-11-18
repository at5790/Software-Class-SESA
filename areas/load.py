#!/usr/bin/env python3
"""
Load census tracts into the areas collection.

raw_data/ holds one Census 2020 Centers of Population tract file per state,
with its content kept exactly as downloaded, named census_tracts_<state>.txt,
such as census_tracts_ny.txt. Every one of them is loaded, so adding a state
means adding its file.

Run from the repo root: python -m areas.load
"""
import csv
import glob
import os

import data.db_connect as dbc
from areas.query import AREAS_COLLECTION
from geo.points import make_point

RAW_DATA = os.path.join(os.path.dirname(__file__), 'raw_data')
TRACT_FILES = sorted(glob.glob(os.path.join(RAW_DATA, 'census_tracts_*.txt')))


def read_areas(file_paths=TRACT_FILES):
    """
    Return one document per tract in the Census files, ready to insert.
    Raises ValueError naming the first row that can't be loaded.
    """
    areas = []
    for file_path in file_paths:
        # utf-8-sig skips the byte-order mark the Census files start with.
        with open(file_path, newline='', encoding='utf-8-sig') as tract_file:
            for row in csv.DictReader(tract_file):
                try:
                    areas.append(_to_doc(row))
                except (KeyError, ValueError) as err:
                    raise ValueError(
                        f'Bad row in {file_path}: {row}') from err
    return areas


def _to_doc(row):
    county_fips = row['STATEFP'] + row['COUNTYFP']
    geoid = county_fips + row['TRACTCE']
    population = int(row['POPULATION'])
    return {
        dbc.MONGO_ID: geoid,
        'geoid': geoid,
        'name': tract_name(row['TRACTCE']),
        'state_fips': row['STATEFP'],
        'county_fips': county_fips,
        'population': population,
        # The MVP aims to reach everyone; see docs/data/geospatial_design.md.
        'target_population': population,
        'location': make_point(row['LATITUDE'], row['LONGITUDE']),
    }


def tract_name(tract_code):
    """
    Return the Census name for a 6-digit tract code, whose last two digits
    are decimals: '000100' is Census Tract 1, '010101' is Census Tract 101.01.
    """
    whole, decimals = int(tract_code[:4]), tract_code[4:]
    suffix = '' if decimals == '00' else f'.{decimals}'
    return f'Census Tract {whole}{suffix}'


def load_areas(db=dbc.SE_DB):
    """
    Replace the areas collection with the tracts in the Census files.
    Returns how many were loaded.
    """
    areas = read_areas()
    dbc.drop(AREAS_COLLECTION, db=db)
    dbc.create_many(AREAS_COLLECTION, areas, db=db)
    return len(areas)


def main():
    count = load_areas()
    print(f'Loaded {count} areas into {dbc.SE_DB}.')


if __name__ == '__main__':
    main()
