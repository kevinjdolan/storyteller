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
  story_idea?: string | null
  desired_themes?: string | null
  key_images?: string | null
  audience_notes?: string | null
  must_have_elements?: string | null
  raw_brief: string
  normalized_summary?: string | null
  normalized_preferences?: NormalizedBriefPreferencesView | null
  planning_notes?: string | null
  accepted_at?: string | null
  updated_at: string
}

export type NormalizedBriefPreferencesView = {
  protagonist_type?: string | null
  setting?: string | null
  emotional_goal?: string | null
  constraint_notes: string[]
  bedtime_safety_concerns: string[]
  candidate_motifs: string[]
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

export type BeatSheetView = {
  id: string
  revision_number: number
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
  job_kind?: string
  status: string
  progress_percent: number
  current_segment_index?: number | null
  attempt_count?: number
  stop_reason?: string | null
  error_message?: string | null
  started_at?: string | null
  completed_at?: string | null
  created_at?: string
  updated_at?: string
}

export type AudioJobView = {
  id: string
  status: string
  voice_key?: string | null
  playback_speed?: number
  include_background_music?: boolean
  music_profile?: string | null
  estimated_duration_seconds?: number | null
  current_segment_index?: number | null
  attempt_count?: number
  stop_reason?: string | null
  error_message?: string | null
  started_at?: string | null
  completed_at?: string | null
  created_at?: string
  updated_at?: string
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

export type SessionExplicitChatCommandId =
  | 'next_stage'
  | 'summarize_plan'
  | 'regenerate_pitches'
  | 'pause_writing'
  | 'resume_writing'

export type SessionExplicitChatCommandSource = 'slash_command' | 'quick_action'

export type SessionExplicitChatCommand = {
  command_id: SessionExplicitChatCommandId
  source: SessionExplicitChatCommandSource
  proposed_actions: ChatToUiActionBatch
}

export type ParseSessionChatIntentRequest = {
  message: string
  explicit_command?: SessionExplicitChatCommand | null
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
  selected_beat_sheet?: BeatSheetView | null
  selected_story_setup?: StorySetupView | null
  latest_composition_job?: CompositionJobView | null
  latest_audio_job?: AudioJobView | null
  active_composition_job?: CompositionJobView | null
  active_audio_job?: AudioJobView | null
  latest_story_asset?: SessionAssetView | null
  latest_audio_asset?: SessionAssetView | null
  agent_context_summary?: string | null
}

export type SessionHydrationMetadata = {
  strategy: 'materialized_only' | 'materialized_with_recent_replay'
  materialized_through_sequence_number?: number | null
  replay_from_sequence_number?: number | null
  replayed_event_count: number
  latest_sequence_number?: number | null
  history_event_count: number
  history_window_truncated: boolean
}

export type SessionHydration = {
  snapshot: SessionSnapshot
  recent_history: SessionHistory
  hydration: SessionHydrationMetadata
}

export type SessionContextUpdateResponse = {
  snapshot: SessionSnapshot
  event: SessionHistoryEvent
}

export type SaveSessionStoryBriefRequest = {
  story_idea?: string | null
  desired_themes?: string | null
  key_images?: string | null
  audience_notes?: string | null
  must_have_elements?: string | null
  raw_brief?: string | null
  normalized_summary?: string | null
  normalized_preferences?: NormalizedBriefPreferencesView | null
  planning_notes?: string | null
  edit_mode?: 'replace' | 'append' | 'merge'
  origin?: string
}

export type SessionStoryBriefResponse = {
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

export function fetchSessionHydration(sessionId: string) {
  return getJson<SessionHydration>(`/api/v1/sessions/${sessionId}/hydrate`)
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

export function saveSessionStoryBrief(
  sessionId: string,
  body: SaveSessionStoryBriefRequest,
) {
  return postJson<SessionStoryBriefResponse>(
    `/api/v1/sessions/${sessionId}/story-brief`,
    body,
  )
}

export function parseSessionChatIntent(
  sessionId: string,
  message: string,
  options?: {
    explicitCommand?: SessionExplicitChatCommand | null
  },
) {
  return postJson<ParsedChatIntentResponse>(
    `/api/v1/sessions/${sessionId}/chat/intents`,
    {
      message,
      explicit_command: options?.explicitCommand ?? null,
    },
  )
}

export function createSession(workingTitle?: string) {
  return postJson<CreateSessionResponse>('/api/v1/sessions', {
    working_title: workingTitle ?? null,
  })
}
