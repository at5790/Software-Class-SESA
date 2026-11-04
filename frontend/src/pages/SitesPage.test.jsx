import { render, screen, within } from '@testing-library/react'
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

test('shows the address, capacity and status of a site', () => {
  render(<SitesPage />)
  const site = mockSites[0]
  const row = screen.getByText(site.name).closest('tr')
  expect(within(row).getByText(site.address)).toBeTruthy()
  expect(within(row).getByText(String(site.capacity))).toBeTruthy()
  expect(within(row).getByText('Active')).toBeTruthy()
})

test('shows inactive for a site that is not active', () => {
  render(<SitesPage />)
  const site = mockSites.find((s) => !s.active)
  const row = screen.getByText(site.name).closest('tr')
  expect(within(row).getByText('Inactive')).toBeTruthy()
})
