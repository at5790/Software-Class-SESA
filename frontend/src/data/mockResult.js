// fake optimizer result in the format from docs/access_contract.md
const mockResult = {
  campaign_id: '1',
  selected_sites: [
    { site_id: 'c1', new_area_ids: ['a2', 'a5', 'a6'], gain: 5200, doses: 400 },
    { site_id: 'c4', new_area_ids: ['a3', 'a8'], gain: 3100, doses: 350 },
    { site_id: 'c7', new_area_ids: ['a9'], gain: 1500, doses: 150 },
  ],
  metrics: {
    baseline_coverage_pct: 62,
    post_coverage_pct: 81.6,
    additional_population: 9800,
    doses_allocated: 900,
    doses_unused: 100,
    sites_selected: 3,
  },
}

export default mockResult
