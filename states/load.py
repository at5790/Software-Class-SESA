#!/usr/bin/env python3
"""
Load the states into the states collection.

The starter's raw_data/states.csv gives each state's code, name and location.
Its FIPS code comes from the Census file raw_data/CenPop2020_Mean_ST.txt,
kept exactly as downloaded, matched by state name.

Run from the repo root: python -m states.load
"""
import csv
import os

import data.db_connect as dbc
from geo.points import make_point
from states.query import STATES_COLLECTION

RAW_DATA = os.path.join(os.path.dirname(__file__), 'raw_data')
STATES_CSV = os.path.join(RAW_DATA, 'states.csv')
CENSUS_STATES = os.path.join(RAW_DATA, 'CenPop2020_Mean_ST.txt')


def read_census_fips(file_path=CENSUS_STATES):
    """Return state name -> FIPS code, from the Census state file."""
    # utf-8-sig skips the byte-order mark the Census file starts with.
    with open(file_path, newline='', encoding='utf-8-sig') as census_file:
        return {row['STNAME']: row['STATEFP']
                for row in csv.DictReader(census_file)}


def read_states(file_path=STATES_CSV, census_path=CENSUS_STATES):
    """
    Return one document per row of the states CSV, ready to insert.
    Raises ValueError naming the first row that can't be loaded.
    """
    fips_by_name = read_census_fips(census_path)
    states = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        for row in csv.DictReader(csvfile):
            try:
                states.append(_to_doc(row, fips_by_name))
            except (KeyError, ValueError) as err:
                raise ValueError(f'Bad row in {file_path}: {row}') from err
    return states


def _to_doc(row, fips_by_name):
    fips = fips_by_name[row['State']]
    return {
        dbc.MONGO_ID: fips,
        'code': row['Abbrev'],
        'name': row['State'],
        'fips': fips,
        'location': make_point(row['Latitude'], row['Longitude']),
    }


def load_states(db=dbc.SE_DB):
    """
    Replace the states collection with the states from raw_data.
    Returns how many were loaded.
    """
    states = read_states()
    dbc.drop(STATES_COLLECTION, db=db)
    dbc.create_many(STATES_COLLECTION, states, db=db)
    return len(states)


def main():
    count = load_states()
    print(f'Loaded {count} states into {dbc.SE_DB}.')


if __name__ == '__main__':
    main()
