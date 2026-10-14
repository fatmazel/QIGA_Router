// VITE_API_URL tanımlı değilse boş string kullanılır; bu durumda istekler
// vite.config.js'deki dev proxy üzerinden yerel backend'e yönlenir.
const BASE = `${import.meta.env.VITE_API_URL ?? ''}/api/v1`

async function post(path, body) {
  const res = await fetch(`${BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail ?? `HTTP ${res.status}`)
  }
  return res.json()
}

export const solveTSP = (params) => post('/solve', params)
export const generateCities = (n, seed) => post('/cities', { n, seed })
