import { render, screen } from '@testing-library/react'
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
