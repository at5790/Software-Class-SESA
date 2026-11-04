import { render, screen } from '@testing-library/react'
import { expect, test } from 'vitest'
import mockSites from '../data/mockSites.js'
import SitesPage from './SitesPage.jsx'

test('shows one list item per site', () => {
  render(<SitesPage />)
  expect(screen.getAllByRole('listitem')).toHaveLength(mockSites.length)
})

test('shows every site name', () => {
  render(<SitesPage />)
  for (const site of mockSites) {
    expect(screen.getByText(site.name)).toBeTruthy()
  }
})
