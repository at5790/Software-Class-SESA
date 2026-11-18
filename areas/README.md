# Area code

This directory contains the code and raw data for areas. Each area is a 2020
census tract.

Raw data (one file per state, all loaded):

- `census_tracts_ny.txt`: Census 2020 tract file for New York.
  Downloaded 2026-11-03 from
  https://www2.census.gov/geo/docs/reference/cenpop2020/tract/CenPop2020_Mean_TR36.txt
  (renamed, not edited)

To load: `python -m areas.load`
