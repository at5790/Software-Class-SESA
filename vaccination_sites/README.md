# Vaccination site code

This directory contains the code and raw data for vaccination sites. Retail
pharmacies are used as the existing vaccination sites.

Raw data:

- `medicaid_pharmacies.csv`: retail pharmacy rows from the NYS Medicaid
  Enrolled Provider Listing (dataset keti-qx5t), only the columns we use.
  Downloaded 2026-11-24 (dataset last updated 2026-11-23) from
  https://health.data.ny.gov/resource/keti-qx5t.csv?$select=mmis_id,npi,mmis_name,service_address,city,state,zip_code,county,latitude,longitude,updated&$where=profession_or_service='PHARMACY'&$limit=50000
  (saved as `keti-qx5t.csv`, renamed, not edited)

To load: `python -m vaccination_sites.load`
