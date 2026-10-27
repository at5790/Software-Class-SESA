// backend url, set VITE_API_URL to point somewhere else
export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// get json from the backend, throws if the request fails
export async function getJson(path) {
  const resp = await fetch(`${API_URL}${path}`)
  if (!resp.ok) {
    throw new Error(`GET ${path} failed with status ${resp.status}`)
  }
  return resp.json()
}

export function getHello() {
  return getJson('/hello')
}

export function getStates() {
  return getJson('/states')
}
