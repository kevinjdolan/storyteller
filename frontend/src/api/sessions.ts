import {
  type WorkflowStageId,
  type WorkflowStageState,
} from '../features/session/workflowStages.ts'
import type { ChatToUiActionBatch } from '../features/session/chat/chatToUiActions.ts'
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

export type SessionEventActorType = 'user' | 'assistant' | 'system' | 'service'

export type SessionEventActor = {
  actor_type: SessionEventActorType
  actor_id?: string | null
}

export type SessionHistoryEvent = {
  id: string
  session_id: string
  sequence_number: number
  actor: SessionEventActor
  event_type: string
  stage?: WorkflowStageId | null
  summary: string
  payload?: Record<string, unknown> | unknown[] | null
  created_at: string
}

export type SessionHistory = {
  session_id: string
  latest_sequence_number?: number | null
  events: SessionHistoryEvent[]
}

export type SessionActionDecision =
  | 'accepted'
  | 'rejected'
  | 'requires_confirmation'
  | 'accepted_with_side_effects'

export type SessionActionPolicyReason = {
  code: string
  message: string
  stage?: WorkflowStageId | null
  related_stages: WorkflowStageId[]
  related_action_types: string[]
}

export type SessionActionPolicySideEffect = {
  kind: string
  message: string
  stages: WorkflowStageId[]
  selection_field?: string | null
  job_kind?: string | null
  asset_kind?: string | null
}

export type SessionActionPolicyEvaluationItem = {
  action_index: number
  action_type: string
  target_stage: WorkflowStageId
  decision: SessionActionDecision
  summary: string
  reasons: SessionActionPolicyReason[]
  side_effects: SessionActionPolicySideEffect[]
  prerequisite_action_types: string[]
}

export type SessionActionPolicyEvaluation = {
  schema_version: number
  session_id: string
  evaluated_actions: SessionActionPolicyEvaluationItem[]
}

export type ParsedChatIntentResponse = {
  schema_version: number
  status: 'parsed' | 'needs_clarification' | 'failed'
  needs_clarification: boolean
  assistant_response: string
  clarification_reason?: string | null
  proposed_actions: ChatToUiActionBatch
  policy_evaluation?: SessionActionPolicyEvaluation | null
}

export type RecordSessionUIActionRequest = {
  action: string
  stage?: WorkflowStageId | null
  control_id?: string | null
  value_summary?: string | null
  origin?: string
}

export type SessionContextStageNoteValues = {
  detail?: string | null
}

export type SessionContextUpdateRequest = {
  target_kind: 'stage_note'
  stage: WorkflowStageId
  control_id?: string | null
  origin?: string
  values: SessionContextStageNoteValues
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
  agent_context_summary?: string | null
}

export type SessionContextUpdateResponse = {
  snapshot: SessionSnapshot
  event: SessionHistoryEvent
}

export type CreateSessionResponse = Pick<SessionSnapshot, 'id'>

export function fetchRecentSessions(limit = 20) {
  return getJson<RecentSessionSummary[]>(`/api/v1/sessions?limit=${limit}`)
}

export function fetchSessionSnapshot(sessionId: string) {
  return getJson<SessionSnapshot>(`/api/v1/sessions/${sessionId}`)
}

export function fetchSessionHistory(sessionId: string) {
  return getJson<SessionHistory>(`/api/v1/sessions/${sessionId}/history`)
}

export function recordSessionUiAction(
  sessionId: string,
  body: RecordSessionUIActionRequest,
) {
  return postJson<SessionHistoryEvent>(
    `/api/v1/sessions/${sessionId}/ui-actions`,
    body,
  )
}

export function applySessionContextUpdate(
  sessionId: string,
  body: SessionContextUpdateRequest,
) {
  return postJson<SessionContextUpdateResponse>(
    `/api/v1/sessions/${sessionId}/context-updates`,
    body,
  )
}

export function parseSessionChatIntent(sessionId: string, message: string) {
  return postJson<ParsedChatIntentResponse>(
    `/api/v1/sessions/${sessionId}/chat/intents`,
    {
      message,
    },
  )
}

export function createSession(workingTitle?: string) {
  return postJson<CreateSessionResponse>('/api/v1/sessions', {
    working_title: workingTitle ?? null,
  })
}
