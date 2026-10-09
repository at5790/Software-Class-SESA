# Access + Optimization data contract

All locations are GeoJSON points: {"type": "Point", "coordinates": [lon, lat]}

area:      {id, population, location}
provider:  {id, active, location}
candidate: {id, capacity, location}
campaign:  {id, radius_km, max_sites, available_doses, unavailable_site_ids?}

optimize(...) returns:
{
  campaign_id,
  selected_sites: [{site_id, new_area_ids, gain, doses}],
  metrics: {baseline_coverage_pct, post_coverage_pct, additional_population,
            doses_allocated, doses_unused, sites_selected}
}

Notes: Mongo's _id is converted to a string "id" before calling these
functions. For the MVP, set max_sites to the number of mobile units.