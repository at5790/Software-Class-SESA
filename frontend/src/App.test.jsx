import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import { expect, test } from 'vitest'
import App from './App.jsx'

// render the app starting at the given url
function renderAt(url) {
  render(
    <MemoryRouter initialEntries={[url]}>
      <App />
    </MemoryRouter>,
  )
}

test('shows the app name and all nav links', () => {
  renderAt('/campaigns')
  expect(screen.getByRole('heading', { name: 'Mobile Vaccination Planner' })).toBeTruthy()
  for (const name of ['Campaigns', 'Sites', 'Map', 'Results']) {
    expect(screen.getByRole('link', { name })).toBeTruthy()
  }
})

test('starts on the campaigns page', () => {
  renderAt('/')
  expect(screen.getByRole('heading', { level: 2, name: 'Campaigns' })).toBeTruthy()
})

test('clicking a nav link opens that page', async () => {
  const user = userEvent.setup()
  renderAt('/campaigns')
  await user.click(screen.getByRole('link', { name: 'Sites' }))
  expect(screen.getByRole('heading', { level: 2, name: 'Sites' })).toBeTruthy()
})
