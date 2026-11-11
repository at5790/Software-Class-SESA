#!/usr/bin/env python3
"""
Load the counties into the counties collection.

raw_data/census_counties.txt is the Census 2020 Centers of Population
county file for the whole US, with its content kept exactly as downloaded.

Run from the repo root: python -m counties.load
"""
import csv
import os

import data.db_connect as dbc
from counties.query import COUNTIES_COLLECTION
from geo.points import make_point

CENSUS_COUNTIES = os.path.join(os.path.dirname(__file__), 'raw_data',
                               'census_counties.txt')


def read_counties(file_path=CENSUS_COUNTIES):
    """
    Return one document per county in the Census file, ready to insert.
    Raises ValueError naming the first row that can't be loaded.
    """
    counties = []
    # utf-8-sig skips the byte-order mark the Census file starts with.
    with open(file_path, newline='', encoding='utf-8-sig') as census_file:
        for row in csv.DictReader(census_file):
            try:
                counties.append(_to_doc(row))
            except (KeyError, ValueError) as err:
                raise ValueError(f'Bad row in {file_path}: {row}') from err
    return counties


def _to_doc(row):
    fips = row['STATEFP'] + row['COUNTYFP']
    return {
        dbc.MONGO_ID: fips,
        'fips': fips,
        'name': row['COUNAME'],
        'state_fips': row['STATEFP'],
        'population': int(row['POPULATION']),
        'location': make_point(row['LATITUDE'], row['LONGITUDE']),
    }


def load_counties(db=dbc.SE_DB):
    """
    Replace the counties collection with the counties in the Census file.
    Returns how many were loaded.
    """
    counties = read_counties()
    dbc.drop(COUNTIES_COLLECTION, db=db)
    dbc.create_many(COUNTIES_COLLECTION, counties, db=db)
    return len(counties)


def main():
    count = load_counties()
    print(f'Loaded {count} counties into {dbc.SE_DB}.')


if __name__ == '__main__':
    main()
