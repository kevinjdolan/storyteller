import {
  type WorkflowStageId,
  type WorkflowStageState,
} from '../features/session/workflowStages.ts'
import { getJson, postJson } from './client.ts'

export type SessionCatalogSelection = {
  id: string
  slug: string
  label: string
}

export type SessionProgress = {
  total_stages: number
  completed_stages: number
  in_progress_stages: number
  needs_regeneration_stages: number
}

export type RecentSessionSummary = {
  id: string
  display_title: string
  working_title?: string | null
  current_stage: WorkflowStageId
  resume_stage: WorkflowStageId
  furthest_completed_stage?: WorkflowStageId | null
  overall_status: WorkflowStageState
  created_at: string
  updated_at: string
  completed_at?: string | null
  selected_genre?: SessionCatalogSelection | null
  selected_tone_profile?: SessionCatalogSelection | null
  progress: SessionProgress
}

export type SessionStageStateView = {
  stage: WorkflowStageId
  label: string
  description: string
  status: WorkflowStageState
  detail?: string | null
  started_at?: string | null
  completed_at?: string | null
  last_event_summary?: string | null
  last_event_type?: string | null
  last_event_at?: string | null
}

export type StoryBriefView = {
  id: string
  revision_number: number
  raw_brief: string
  normalized_summary?: string | null
  planning_notes?: string | null
  accepted_at?: string | null
}

export type PitchView = {
  id: string
  generation_key: string
  pitch_index: number
  title: string
  logline: string
  summary?: string | null
  bedtime_notes?: string | null
  accepted_at?: string | null
}

export type CharacterSheetView = {
  id: string
  revision_number: number
  title?: string | null
  protagonist_name?: string | null
  summary?: string | null
  bedtime_notes?: string | null
  accepted_at?: string | null
}

export type StorySetupView = {
  id: string
  revision_number: number
  target_word_count?: number | null
  target_runtime_minutes?: number | null
  chapter_count?: number | null
  chapter_style?: string | null
  guidance_notes?: string | null
  accepted_at?: string | null
}

export type CompositionJobView = {
  id: string
  status: string
  progress_percent: number
  current_segment_index?: number | null
}

export type AudioJobView = {
  id: string
  status: string
  voice_key?: string | null
  estimated_duration_seconds?: number | null
}

export type SessionAssetView = {
  id: string
  asset_kind: string
  status: string
  ready_at?: string | null
}

export type SessionSnapshot = RecentSessionSummary & {
  stage_states: SessionStageStateView[]
  story_brief?: StoryBriefView | null
  selected_pitch?: PitchView | null
  selected_character_sheet?: CharacterSheetView | null
  selected_story_setup?: StorySetupView | null
  active_composition_job?: CompositionJobView | null
  active_audio_job?: AudioJobView | null
  latest_story_asset?: SessionAssetView | null
  latest_audio_asset?: SessionAssetView | null
}

export type CreateSessionResponse = Pick<SessionSnapshot, 'id'>

export function fetchRecentSessions(limit = 20) {
  return getJson<RecentSessionSummary[]>(`/api/v1/sessions?limit=${limit}`)
}

export function fetchSessionSnapshot(sessionId: string) {
  return getJson<SessionSnapshot>(`/api/v1/sessions/${sessionId}`)
}

export function createSession(workingTitle?: string) {
  return postJson<CreateSessionResponse>('/api/v1/sessions', {
    working_title: workingTitle ?? null,
  })
}
