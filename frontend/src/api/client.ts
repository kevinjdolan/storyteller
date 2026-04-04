const apiBaseUrl = (import.meta.env.VITE_API_URL ?? '').replace(/\/+$/, '')

export function resolveApiUrl(path: `/${string}`) {
  return `${apiBaseUrl}${path}`
}

async function parseJsonResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    throw new Error(`Unexpected status code: ${response.status}`)
  }

  return (await response.json()) as T
}

export async function getJson<T>(path: `/${string}`): Promise<T> {
  const response = await fetch(resolveApiUrl(path))

  return parseJsonResponse<T>(response)
}

export async function postJson<T>(
  path: `/${string}`,
  body?: unknown,
): Promise<T> {
  const response = await fetch(resolveApiUrl(path), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: body === undefined ? undefined : JSON.stringify(body),
  })

  return parseJsonResponse<T>(response)
}
