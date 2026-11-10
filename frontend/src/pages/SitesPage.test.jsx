import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { expect, test } from 'vitest'
import mockSites from '../data/mockSites.js'
import SitesPage from './SitesPage.jsx'

test('shows one table row per site', () => {
  render(<SitesPage />)
  // +1 for the header row
  expect(screen.getAllByRole('row')).toHaveLength(mockSites.length + 1)
})

test('shows every site name', () => {
  render(<SitesPage />)
  for (const site of mockSites) {
    expect(screen.getByText(site.name)).toBeTruthy()
  }
})

test('adding a site puts a new active row in the table', async () => {
  const user = userEvent.setup()
  render(<SitesPage />)
  await user.type(screen.getByLabelText('Name'), 'New Clinic')
  await user.type(screen.getByLabelText('Address'), '5 New St')
  await user.type(screen.getByLabelText('Capacity'), '80')
  await user.click(screen.getByRole('button', { name: 'Add site' }))
  expect(screen.getAllByRole('row')).toHaveLength(mockSites.length + 2)
  const row = screen.getByText('New Clinic').closest('tr')
  expect(within(row).getByText('Active')).toBeTruthy()
})
