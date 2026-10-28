# State code

This directory contains *code*, *raw data*, and *JSON files* for the state part of our
project.

`raw_data/` holds two files:

- `states.csv`, from the starter repo: each state's code, name and location,
  for the 50 states, DC and Puerto Rico.
- `CenPop2020_Mean_ST.txt`, the Census 2020 Centers of Population state file,
  kept exactly as downloaded from
  https://www2.census.gov/geo/docs/reference/cenpop2020/CenPop2020_Mean_ST.txt
  on 2026-10-27. Its FIPS codes are matched to `states.csv` by state name
  when loading.

Load the states into MongoDB from the repo root with `python -m states.load`.
