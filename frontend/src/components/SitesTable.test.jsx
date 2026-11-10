import { render, screen, within } from '@testing-library/react'
import { expect, test } from 'vitest'
import SitesTable from './SitesTable.jsx'

const SITES = [
  { id: 'a', name: 'Test Clinic', address: '1 Test St', capacity: 50, active: true },
  { id: 'b', name: 'Closed Clinic', address: '2 Test St', capacity: 75, active: false },
]

// find the table row that has this site name
function rowFor(name) {
  return screen.getByText(name).closest('tr')
}

test('shows one row per site plus the header', () => {
  render(<SitesTable sites={SITES} />)
  expect(screen.getAllByRole('row')).toHaveLength(SITES.length + 1)
})

test('shows the address, capacity and status of a site', () => {
  render(<SitesTable sites={SITES} />)
  const row = rowFor('Test Clinic')
  expect(within(row).getByText('1 Test St')).toBeTruthy()
  expect(within(row).getByText('50')).toBeTruthy()
  expect(within(row).getByText('Active')).toBeTruthy()
})

test('shows inactive for a site that is not active', () => {
  render(<SitesTable sites={SITES} />)
  expect(within(rowFor('Closed Clinic')).getByText('Inactive')).toBeTruthy()
})

test('shows only the header when there are no sites', () => {
  render(<SitesTable sites={[]} />)
  expect(screen.getAllByRole('row')).toHaveLength(1)
})
