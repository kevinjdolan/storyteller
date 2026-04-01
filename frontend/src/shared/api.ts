const apiBaseUrl = (import.meta.env.VITE_API_URL ?? '').replace(/\/+$/, '')

export function resolveApiUrl(path: `/${string}`) {
  return `${apiBaseUrl}${path}`
}
