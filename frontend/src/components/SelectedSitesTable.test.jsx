import { render, screen, within } from '@testing-library/react'
import { expect, test } from 'vitest'
import SelectedSitesTable from './SelectedSitesTable.jsx'

const SITES = [
  { site_id: 's1', new_area_ids: ['a1', 'a2'], gain: 4500, doses: 300 },
  { site_id: 's2', new_area_ids: ['a3'], gain: 800, doses: 50 },
]

test('shows one row per selected site plus the header', () => {
  render(<SelectedSitesTable sites={SITES} />)
  expect(screen.getAllByRole('row')).toHaveLength(SITES.length + 1)
})

test('shows people reached, doses and areas for a site', () => {
  render(<SelectedSitesTable sites={SITES} />)
  const row = screen.getByText('s1').closest('tr')
  expect(within(row).getByText('4,500')).toBeTruthy()
  expect(within(row).getByText('300')).toBeTruthy()
  // two area ids, so two areas covered
  expect(within(row).getByText('2')).toBeTruthy()
})

test('shows a message when no sites were selected', () => {
  render(<SelectedSitesTable sites={[]} />)
  expect(screen.getByText('No sites selected')).toBeTruthy()
  expect(screen.queryByRole('table')).toBeNull()
})
