const apiBaseUrl = (import.meta.env.VITE_API_URL ?? '').replace(/\/+$/, '')

export function resolveApiUrl(path: `/${string}`) {
  return `${apiBaseUrl}${path}`
}

export async function getJson<T>(path: `/${string}`): Promise<T> {
  const response = await fetch(resolveApiUrl(path))

  if (!response.ok) {
    throw new Error(`Unexpected status code: ${response.status}`)
  }

  return (await response.json()) as T
}
