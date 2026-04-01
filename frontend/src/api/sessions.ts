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

export type CreateSessionResponse = {
  id: string
}

export function fetchRecentSessions(limit = 20) {
  return getJson<RecentSessionSummary[]>(`/api/v1/sessions?limit=${limit}`)
}

export function createSession(workingTitle?: string) {
  return postJson<CreateSessionResponse>('/api/v1/sessions', {
    working_title: workingTitle ?? null,
  })
}
