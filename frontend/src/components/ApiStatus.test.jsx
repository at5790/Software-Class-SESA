import { render, screen } from '@testing-library/react'
import { afterEach, expect, test, vi } from 'vitest'
import ApiStatus from './ApiStatus.jsx'

afterEach(() => {
  vi.unstubAllGlobals()
})

test('shows checking while waiting for the backend', () => {
  // fetch that never answers
  vi.stubGlobal('fetch', vi.fn(() => new Promise(() => {})))
  render(<ApiStatus />)
  expect(screen.getByText('Checking API…')).toBeTruthy()
})

test('shows connected when the backend answers', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue({
    ok: true,
    status: 200,
    json: async () => ({ hello: 'world' }),
  }))
  render(<ApiStatus />)
  expect(await screen.findByText('API connected')).toBeTruthy()
})

test('shows not connected when the backend is down', async () => {
  vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new TypeError('Failed to fetch')))
  render(<ApiStatus />)
  expect(await screen.findByText('API not connected')).toBeTruthy()
})
