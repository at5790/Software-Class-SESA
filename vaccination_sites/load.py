#!/usr/bin/env python3
"""
Load pharmacies into the vaccination_sites collection.

raw_data/medicaid_pharmacies.csv holds the pharmacy rows of the NYS Medicaid
Enrolled Provider Listing, with its content kept exactly as downloaded.
Rows that can't be used are skipped and counted by reason.

Run from the repo root: python -m vaccination_sites.load
"""
import collections
import csv
import os

import data.db_connect as dbc
from areas.load import read_areas
from counties.load import read_counties
from geo.distance import distance_km
from geo.points import make_point
from states.load import read_states
from vaccination_sites.query import SITES_COLLECTION

MEDICAID_PHARMACIES = os.path.join(os.path.dirname(__file__), 'raw_data',
                                   'medicaid_pharmacies.csv')

DEFAULT_CAPACITY = 100  # the optimizer doesn't use it
MAX_KM_FROM_COUNTY = 100
BORDER_KM = 10  # out-of-state sites this close to an area are kept

# Values in the listing
CLOSED_CHAIN = 'RITE AID'  # closed all its stores in 2025
OUT_OF_STATE = 'OUT OF STATE'  # the county given outside New York

# Why a row is skipped
CLOSED = f'{CLOSED_CHAIN} (closed)'
BAD_LOCATION = f'invalid or over {MAX_KM_FROM_COUNTY} km from its county'
NOT_NEAR_AREA = f'out of state and over {BORDER_KM} km from every area'
REPEAT = 'same pharmacy at the same location'


def county_key(name):
    """Match 'St. Lawrence' (Census) with 'ST LAWRENCE' (the listing)."""
    return name.upper().replace('.', '').replace(' ', '')


def read_sites(file_path=MEDICAID_PHARMACIES):
    """
    Return (sites, skipped): a document for each usable row, and a
    (reason, row) pair for each skipped row.
    """
    state_codes = {state['fips']: state['code'] for state in read_states()}
    counties = collections.defaultdict(list)  # state code -> its counties
    for county in read_counties():
        counties[state_codes[county['state_fips']]].append(county)
    area_points = [area['location'] for area in read_areas()]

    sites, skipped, loaded = [], [], set()
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        for row in csv.DictReader(csvfile):
            # Different pharmacies can share coordinates, so include the ID.
            key = (row['mmis_id'], row['latitude'], row['longitude'])
            if key in loaded:
                site, reason = None, REPEAT
            else:
                site, reason = _to_doc(row, counties[row['state']],
                                       area_points)
            if site:
                loaded.add(key)
                sites.append(site)
            else:
                skipped.append((reason, row))
    return sites, skipped


def _to_doc(row, counties, area_points):
    """
    Return (site, None), or (None, reason) if the row is skipped.
    counties are those in the row's state.
    """
    if CLOSED_CHAIN in row['mmis_name'].upper():
        return None, CLOSED
    try:
        location = make_point(row['latitude'], row['longitude'])
    except ValueError:
        return None, BAD_LOCATION
    if row['county'] == OUT_OF_STATE:
        if all(distance_km(location, p) > BORDER_KM for p in area_points):
            return None, NOT_NEAR_AREA
        county = min(counties,
                     key=lambda c: distance_km(location, c['location']))
    else:
        name = county_key(row['county'])
        county = next((c for c in counties if county_key(c['name']) == name),
                      None)
        if (not county or distance_km(location, county['location'])
                > MAX_KM_FROM_COUNTY):
            return None, BAD_LOCATION
    return {
        'name': row['mmis_name'],
        'address': (f"{row['service_address']}, {row['city']}, "
                    f"{row['state']} {row['zip_code']}"),
        'state_fips': county['state_fips'],
        'county_fips': county['fips'],
        'location': location,
        'capacity': DEFAULT_CAPACITY,
        'active': True,
    }, None


def load_sites(db=dbc.SE_DB):
    """
    Replace the vaccination_sites collection with the usable pharmacies.
    Returns how many were loaded and the skipped (reason, row) pairs.
    """
    sites, skipped = read_sites()
    dbc.drop(SITES_COLLECTION, db=db)
    dbc.create_many(SITES_COLLECTION, sites, db=db)
    return len(sites), skipped


def main():
    count, skipped = load_sites()
    print(f'Loaded {count} vaccination sites into {dbc.SE_DB}.')
    for reason, n in collections.Counter(r for r, _ in skipped).items():
        print(f'Skipped {n}: {reason}')


if __name__ == '__main__':
    main()
