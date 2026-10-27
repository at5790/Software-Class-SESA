import { afterEach, expect, test, vi } from 'vitest'
import { API_URL, getHello, getJson, getStates } from './client.js'

// swap in a fake fetch that returns the given status and body
function mockFetch(status, body) {
  const fetchMock = vi.fn().mockResolvedValue({
    ok: status >= 200 && status < 300,
    status,
    json: async () => body,
  })
  vi.stubGlobal('fetch', fetchMock)
  return fetchMock
}

afterEach(() => {
  vi.unstubAllGlobals()
})

test('getJson returns the response data', async () => {
  mockFetch(200, { hello: 'world' })
  expect(await getJson('/hello')).toEqual({ hello: 'world' })
})

test('getJson calls the backend url', async () => {
  const fetchMock = mockFetch(200, {})
  await getJson('/states')
  expect(fetchMock).toHaveBeenCalledWith(`${API_URL}/states`)
})

test('getJson throws when the backend returns an error', async () => {
  mockFetch(500, {})
  await expect(getJson('/hello')).rejects.toThrow('500')
})

test('getJson throws when the backend is down', async () => {
  vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new TypeError('Failed to fetch')))
  await expect(getJson('/hello')).rejects.toThrow('Failed to fetch')
})

test('getHello and getStates call the right endpoints', async () => {
  const fetchMock = mockFetch(200, {})
  await getHello()
  await getStates()
  expect(fetchMock).toHaveBeenNthCalledWith(1, `${API_URL}/hello`)
  expect(fetchMock).toHaveBeenNthCalledWith(2, `${API_URL}/states`)
})
