import { getJson, postJson } from './client.ts'

export type GenreCatalogArcNotes = Record<string, string | number | boolean>

export type GenreCatalogEntry = {
  id: string
  slug: string
  label: string
  description?: string | null
  bedtime_safety_notes?: string | null
  arc_notes: GenreCatalogArcNotes
  sort_order: number
}

export type ToneCatalogEntry = {
  id: string
  genre_id: string
  slug: string
  label: string
  description?: string | null
  bedtime_notes?: string | null
  descriptors: string[]
  default_planning_hints: Record<string, unknown>
  sort_order: number
}

export type SelectSessionGenreRequest = {
  genre_id?: string | null
  genre_slug?: string | null
  genre_label?: string | null
  origin?: string
}

export type SelectSessionToneRequest = {
  tone_profile_id?: string | null
  tone_profile_slug?: string | null
  tone_profile_label?: string | null
  origin?: string
}

export type SessionSelectionResponse<TSnapshot, TEvent> = {
  snapshot: TSnapshot
  event: TEvent
}

export function fetchGenreCatalog() {
  return getJson<GenreCatalogEntry[]>('/api/v1/catalog/genres')
}

export function fetchToneCatalogForGenre(genreSlug: string) {
  return getJson<ToneCatalogEntry[]>(
    `/api/v1/catalog/genres/${encodeURIComponent(genreSlug)}/tones`,
  )
}

export function selectSessionGenre<TSnapshot, TEvent>(
  sessionId: string,
  body: SelectSessionGenreRequest,
) {
  return postJson<SessionSelectionResponse<TSnapshot, TEvent>>(
    `/api/v1/sessions/${sessionId}/selections/genre`,
    body,
  )
}

export function selectSessionTone<TSnapshot, TEvent>(
  sessionId: string,
  body: SelectSessionToneRequest,
) {
  return postJson<SessionSelectionResponse<TSnapshot, TEvent>>(
    `/api/v1/sessions/${sessionId}/selections/tone`,
    body,
  )
}
