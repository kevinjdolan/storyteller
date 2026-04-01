import { getJson } from './client.ts'

export type BackendHelloResponse = {
  message?: string
}

export function fetchBackendHello() {
  return getJson<BackendHelloResponse>('/api/hello')
}
