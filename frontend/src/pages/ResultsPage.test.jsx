import { render, screen, within } from '@testing-library/react'
import { expect, test } from 'vitest'
import mockResult from '../data/mockResult.js'
import ResultsPage from './ResultsPage.jsx'

// the box that has this label
function statFor(label) {
  return screen.getByText(label).closest('.stat')
}

test('shows coverage before and after', () => {
  render(<ResultsPage />)
  expect(within(statFor('Coverage before')).getByText('62%')).toBeTruthy()
  expect(within(statFor('Coverage after')).getByText('81.6%')).toBeTruthy()
})

test('shows people reached with a comma', () => {
  render(<ResultsPage />)
  expect(within(statFor('People newly reached')).getByText('9,800')).toBeTruthy()
})

test('shows sites selected and doses', () => {
  render(<ResultsPage />)
  expect(within(statFor('Sites selected')).getByText('3')).toBeTruthy()
  expect(within(statFor('Doses allocated')).getByText('900')).toBeTruthy()
  expect(within(statFor('Doses unused')).getByText('100')).toBeTruthy()
})

test('shows a table row for each selected site', () => {
  render(<ResultsPage />)
  for (const site of mockResult.selected_sites) {
    expect(screen.getByRole('cell', { name: site.site_id })).toBeTruthy()
  }
})
