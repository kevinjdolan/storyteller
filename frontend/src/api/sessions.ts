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
  hook?: string | null
  central_conflict?: string | null
  why_it_fits?: string | null
  logline: string
  summary?: string | null
  bedtime_notes?: string | null
  generation_kind?: string
  source_pitch_id?: string | null
  source_pitch_title?: string | null
  refinement_instructions?: string | null
  selection_rationale?: string | null
  is_selected?: boolean
  accepted_at?: string | null
  created_at?: string
  updated_at?: string
}

export type PitchBatchView = {
  generation_key: string
  candidate_count: number
  created_at: string
  generation_kind?: string
  guidance?: string | null
  source_pitch_id?: string | null
  source_pitch_title?: string | null
  source_generation_key?: string | null
  refinement_instructions?: string | null
  pitches: PitchView[]
}

export type BeatSheetBeatView = {
  key: string
  label: string
  order: number
  summary: string
  emotional_intent?: string | null
  bedtime_softening_note?: string | null
}

export type BeatSheetEditView = {
  id: string
  summary_text: string
  origin: string
  changed_fields: string[]
  beat_keys: string[]
  material_change: boolean
  refreshes_downstream: boolean
  created_at: string
}

export type BeatSheetView = {
  id: string
  revision_number: number
  generation_kind?: string
  summary?: string | null
  beats: BeatSheetBeatView[]
  bedtime_notes?: string | null
  source_beat_sheet_id?: string | null
  source_beat_sheet_revision_number?: number | null
  guidance?: string | null
  refinement_instructions?: string | null
  focus_beats: string[]
  bedtime_goal?: string | null
  selection_rationale?: string | null
  edit_history?: BeatSheetEditView[] | null
  is_selected?: boolean
  accepted_at?: string | null
  created_at?: string
  updated_at?: string
}

export type CharacterProfileView = {
  name: string
  role?: string | null
  goal?: string | null
  flaw?: string | null
  comfort_trait?: string | null
  bedtime_safety_notes?: string | null
  relationships: string[]
  visual_anchors: string[]
}

export type CharacterSheetView = {
  id: string
  revision_number: number
  generation_key?: string | null
  candidate_index?: number | null
  title?: string | null
  protagonist_name?: string | null
  summary?: string | null
  story_function?: string | null
  protagonist?: CharacterProfileView | null
  supporting_cast: CharacterProfileView[]
  bedtime_notes?: string | null
  bedtime_safety_notes?: string | null
  visual_motifs: string[]
  generation_kind?: string
  source_pitch_id?: string | null
  source_pitch_title?: string | null
  source_character_sheet_id?: string | null
  source_character_sheet_title?: string | null
  refinement_instructions?: string | null
  focus_character_names?: string[]
  change_summary?: string | null
  change_impact?: 'minor' | 'major' | null
  selection_rationale?: string | null
  is_selected?: boolean
  accepted_at?: string | null
  created_at?: string
  updated_at?: string
}

export type CharacterSheetBatchView = {
  generation_key: string
  candidate_count: number
  created_at: string
  generation_kind?: string
  guidance?: string | null
  source_pitch_id?: string | null
  source_pitch_title?: string | null
  source_character_sheet_id?: string | null
  source_character_sheet_title?: string | null
  refinement_instructions?: string | null
  focus_character_names?: string[]
  change_summary?: string | null
  change_impact?: 'minor' | 'major' | null
  character_sheets: CharacterSheetView[]
}

export type StorySetupView = {
  id: string
  revision_number: number
  target_word_count?: number | null
  target_runtime_minutes?: number | null
  chapter_count?: number | null
  approximate_scene_count?: number | null
  chapter_style?: string | null
  guidance_notes?: string | null
  accepted_at?: string | null
}

export type ContinuityFactView = {
  key: string
  category:
    | 'character'
    | 'location'
    | 'object'
    | 'promise'
    | 'voice_constraint'
    | 'unresolved_thread'
    | 'locked_detail'
  title: string
  detail: string
  source_stage?: WorkflowStageId | null
  source_label?: string | null
}

export type ContinuityBibleView = {
  id: string
  revision_number: number
  source_stage?: WorkflowStageId | null
  source_summary?: string | null
  summary_text: string
  facts: ContinuityFactView[]
  created_at: string
  updated_at: string
}

export type StoryOutlineCard = {
  card_key: string
  card_type: 'chapter' | 'scene'
  position: number
  title: string
  purpose?: string | null
  summary: string
  beat_keys: string[]
  beat_labels: string[]
  emotional_shift: string
  target_word_count?: number | null
  target_runtime_minutes?: number | null
  target_scene_count?: number | null
  tone_direction?: string | null
  bedtime_guardrail?: string | null
  drafting_brief?: string | null
}

export type StoryOutlineEditView = {
  summary_text: string
  origin: string
  changed_fields: string[]
  changed_card_keys: string[]
  regenerated_card_keys: string[]
  change_impact?: 'minor' | 'major' | null
  reordered: boolean
  refreshes_downstream: boolean
  invalidated_stages: WorkflowStageId[]
  created_at: string
}

export type StoryOutlineView = {
  id: string
  revision_number: number
  outline_kind: 'chapter' | 'scene'
  summary?: string | null
  cards: StoryOutlineCard[]
  genre_label?: string | null
  tone_label?: string | null
  target_word_count?: number | null
  target_runtime_minutes?: number | null
  chapter_count?: number | null
  approximate_scene_count?: number | null
  chapter_style?: string | null
  guidance_notes?: string | null
  bedtime_goal?: string | null
  last_change_summary?: string | null
  change_impact?: 'minor' | 'major' | null
  refreshes_downstream?: boolean
  invalidated_stages?: WorkflowStageId[]
  edit_history?: StoryOutlineEditView[]
  is_selected?: boolean
  accepted_at?: string | null
  created_at?: string | null
  updated_at?: string | null
}

export type PlanArtifactRefView = {
  id: string
  label: string
  revision_number?: number | null
}

export type PlanRevisionView = {
  id: string
  revision_number: number
  source_stage?: WorkflowStageId | null
  change_summary?: string | null
  comparison_summary?: string | null
  restored_from_revision_number?: number | null
  changed_artifacts: string[]
  pitch?: PlanArtifactRefView | null
  character_sheet?: PlanArtifactRefView | null
  beat_sheet?: PlanArtifactRefView | null
  story_setup?: PlanArtifactRefView | null
  story_outline?: PlanArtifactRefView | null
  is_current?: boolean
  created_at: string
  updated_at: string
}

export type CompositionInterruptionRequestView = {
  id: string
  request_kind: string
  state: string
  origin: string
  message: string
  instructions?: string | null
  rewrite_from_segment_index?: number | null
  requested_status?: string | null
  requested_segment_id?: string | null
  requested_segment_index?: number | null
  requested_progress_percent?: number | null
  resolution_summary?: string | null
  created_at: string
  updated_at: string
  resolved_at?: string | null
}

export type CompositionJobView = {
  id: string
  job_kind?: string
  status: string
  progress_percent: number
  start_segment_index?: number | null
  plan_revision_id?: string | null
  plan_revision_number?: number | null
  beat_sheet_id?: string | null
  beat_sheet_revision_number?: number | null
  story_setup_id?: string | null
  story_setup_revision_number?: number | null
  story_outline_id?: string | null
  story_outline_revision_number?: number | null
  current_segment_id?: string | null
  current_segment_index?: number | null
  total_segments?: number | null
  rewrite_to_segment_index?: number | null
  downstream_regeneration_mode?: 'none' | 'auto_regenerate' | 'require_confirmation'
  stale_from_segment_index?: number | null
  stale_to_segment_index?: number | null
  pending_review?: boolean
  rewrite_candidate_segment_indexes?: number[]
  accepted_story_so_far?: string | null
  latest_partial_output?: string | null
  latest_segment_summary?: string | null
  interruption_request?: CompositionInterruptionRequestView | null
  attempt_count?: number
  stop_reason?: string | null
  error_message?: string | null
  started_at?: string | null
  completed_at?: string | null
  created_at?: string
  updated_at?: string
}

export type CompositionSegmentVersionView = {
  id: string
  composition_job_id: string
  job_kind: string
  segment_index: number
  revision_number: number
  status: string
  acceptance_state: 'accepted' | 'pending' | 'rejected'
  is_current: boolean
  is_stale: boolean
  planned_summary?: string | null
  accepted_summary?: string | null
  text_content?: string | null
  word_count?: number | null
  created_at: string
  updated_at: string
  completed_at?: string | null
}

export type CompositionSegmentView = {
  segment_index: number
  outline_card_title?: string | null
  outline_card_summary?: string | null
  current_version_id?: string | null
  current_revision_number?: number | null
  pending_version_id?: string | null
  pending_revision_number?: number | null
  is_stale: boolean
  stale_reason?: string | null
  versions: CompositionSegmentVersionView[]
}

export type AudioJobView = {
  id: string
  status: string
  voice_key?: string | null
  playback_speed?: number
  include_background_music?: boolean
  music_profile?: string | null
  progress_percent?: number
  current_step?: string | null
  current_step_index?: number | null
  total_steps?: number | null
  completed_segments?: number | null
  estimated_duration_seconds?: number | null
  total_segments?: number | null
  current_segment_index?: number | null
  latest_asset_id?: string | null
  latest_asset_kind?: string | null
  attempt_count?: number
  stop_reason?: string | null
  error_message?: string | null
  started_at?: string | null
  completed_at?: string | null
  created_at?: string
  updated_at?: string
}

export type AudioRuntimeEstimateView = {
  estimated_word_count: number
  estimated_chapter_count: number
  chapter_pause_count: number
  chapter_pause_seconds: number
  total_chapter_pause_seconds: number
  assumed_words_per_minute: number
  minimum_words_per_minute: number
  maximum_words_per_minute: number
  target_duration_seconds: number
  minimum_duration_seconds: number
  maximum_duration_seconds: number
  basis_source: 'composition_segments' | 'story_setup_target' | 'unknown'
  pacing_band: 'roomy' | 'balanced' | 'brisk'
}

export type AudioMusicProfileOptionView = {
  key: 'lullaby_piano' | 'string_drift' | 'night_ambience'
  label: string
  description: string
  bedtime_use_case: string
  asset_file_name: string
  loop_duration_seconds: number
  recommended_music_volume: number
  recommended_music_volume_min: number
  recommended_music_volume_max: number
  mix_note: string
}

export type AudioMixPreviewView = {
  strategy: 'voice_only' | 'curated_bed_ducked'
  summary: string
  track_key?: AudioMusicProfileOptionView['key'] | null
  track_label?: string | null
  track_description?: string | null
  narration_gain_db: number
  music_gain_db?: number | null
  ducking_ratio?: number | null
  ducking_threshold?: number | null
  fade_out_seconds?: number | null
  loop_duration_seconds?: number | null
}

export type AudioSettingsView = {
  voice_key: 'moonbeam' | 'hearthside' | 'storykeeper'
  narration_style: 'calm' | 'hushed' | 'warm'
  playback_speed: number
  include_background_music: boolean
  music_profile: 'lullaby_piano' | 'string_drift' | 'night_ambience'
  narration_volume: number
  music_volume: number
  guidance_notes?: string | null
  music_profile_options?: AudioMusicProfileOptionView[] | null
  mix_preview?: AudioMixPreviewView | null
  runtime_estimate?: AudioRuntimeEstimateView | null
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

export type SaveSessionAudioSettingsRequest = {
  voice_key?: AudioSettingsView['voice_key'] | null
  narration_style?: AudioSettingsView['narration_style'] | null
  playback_speed?: number | null
  include_background_music?: boolean | null
  music_profile?: AudioSettingsView['music_profile'] | null
  narration_volume?: number | null
  music_volume?: number | null
  guidance_notes?: string | null
  origin?: string
}

export type EditSessionBeatSheetBeatRequest = {
  key: string
  summary?: string | null
  emotional_intent?: string | null
  bedtime_softening_note?: string | null
}

export type EditSessionBeatSheetRequest = {
  beat_sheet_id?: string | null
  revision_number?: number | null
  summary?: string | null
  bedtime_notes?: string | null
  bedtime_goal?: string | null
  beat_updates?: EditSessionBeatSheetBeatRequest[]
  summary_text?: string | null
  origin?: string
}

export type SessionSnapshot = RecentSessionSummary & {
  stage_states: SessionStageStateView[]
  story_brief?: StoryBriefView | null
  pitch_batches?: PitchBatchView[] | null
  selected_pitch?: PitchView | null
  character_sheet_batches?: CharacterSheetBatchView[] | null
  selected_character_sheet?: CharacterSheetView | null
  beat_sheet_revisions?: BeatSheetView[] | null
  selected_beat_sheet?: BeatSheetView | null
  selected_story_setup?: StorySetupView | null
  story_outline_revisions?: StoryOutlineView[] | null
  selected_story_outline?: StoryOutlineView | null
  plan_revisions?: PlanRevisionView[] | null
  current_plan_revision?: PlanRevisionView | null
  latest_composition_job?: CompositionJobView | null
  latest_audio_job?: AudioJobView | null
  active_composition_job?: CompositionJobView | null
  active_audio_job?: AudioJobView | null
  composition_segments?: CompositionSegmentView[] | null
  latest_story_asset?: SessionAssetView | null
  latest_audio_asset?: SessionAssetView | null
  audio_settings?: AudioSettingsView | null
  continuity_bible?: ContinuityBibleView | null
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

export type SessionAudioSettingsResponse = {
  snapshot: SessionSnapshot
  event: SessionHistoryEvent
}

export type SessionBeatSheetUpdateResponse = {
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

export type GenerateSessionPitchesRequest = {
  candidate_count?: number
  guidance?: string | null
  preserve_selected_pitch?: boolean
  origin?: string
}

export type GenerateSessionCharacterSheetsRequest = {
  candidate_count?: number
  guidance?: string | null
  origin?: string
}

export type GenerateSessionBeatSheetRequest = {
  guidance?: string | null
  focus_beats?: string[]
  bedtime_goal?: string | null
  origin?: string
}

export type SaveSessionStorySetupRequest = {
  target_word_count?: number | null
  target_runtime_minutes?: number | null
  chapter_count?: number | null
  approximate_scene_count?: number | null
  guidance_notes?: string | null
  origin?: string
}

export type SaveSessionStoryOutlineRequest = {
  outline_id?: string | null
  summary?: string | null
  cards: StoryOutlineCard[]
  regenerate_card_keys?: string[]
  origin?: string
}

export type StartSessionCompositionRequest = {
  mode?: 'fresh' | 'continue' | 'rewrite'
  instructions?: string | null
  restart_from_segment_index?: number | null
  rewrite_to_segment_index?: number | null
  downstream_regeneration_mode?: 'none' | 'auto_regenerate' | 'require_confirmation' | null
  origin?: string
}

export type RedirectSessionCompositionRequest = {
  instructions: string
  rewrite_from_segment_index?: number | null
  rewrite_to_segment_index?: number | null
  downstream_regeneration_mode?: 'none' | 'auto_regenerate' | 'require_confirmation' | null
  origin?: string
}

export type AcceptRewriteSessionCompositionRequest = {
  origin?: string
}

export type RejectRewriteSessionCompositionRequest = {
  origin?: string
}

export type SelectCompositionSegmentVersionRequest = {
  origin?: string
}

export type SelectSessionPitchRequest = {
  pitch_id?: string | null
  generation_key?: string | null
  pitch_index?: number | null
  title?: string | null
  origin?: string
}

export type SelectSessionCharacterSheetRequest = {
  character_sheet_id?: string | null
  revision_number?: number | null
  title?: string | null
  origin?: string
}

export type SelectSessionBeatSheetRequest = {
  beat_sheet_id?: string | null
  revision_number?: number | null
  origin?: string
}

export type RefineSessionPitchRequest = {
  pitch_id?: string | null
  generation_key?: string | null
  pitch_index?: number | null
  title?: string | null
  instructions: string
  origin?: string
}

export type RefineSessionCharacterSheetRequest = {
  character_sheet_id?: string | null
  revision_number?: number | null
  title?: string | null
  instructions: string
  focus_character_names?: string[]
  change_summary?: string | null
  change_impact?: 'minor' | 'major' | null
  origin?: string
}

export type RefineSessionBeatSheetRequest = {
  beat_sheet_id?: string | null
  revision_number?: number | null
  instructions: string
  beat_names?: string[]
  bedtime_goal?: string | null
  origin?: string
}

export type RestoreSessionPlanRevisionRequest = {
  origin?: string
}

export type SessionPitchGenerationResponse = {
  snapshot: SessionSnapshot
  event: SessionHistoryEvent
}

export type SessionCharacterSheetGenerationResponse = {
  snapshot: SessionSnapshot
  event: SessionHistoryEvent
}

export type SessionBeatSheetGenerationResponse = {
  snapshot: SessionSnapshot
  event: SessionHistoryEvent
}

export type SessionStorySetupResponse = {
  snapshot: SessionSnapshot
  event: SessionHistoryEvent
}

export type SessionStoryOutlineResponse = {
  snapshot: SessionSnapshot
  event: SessionHistoryEvent
}

export type SessionCompositionResponse = {
  snapshot: SessionSnapshot
  event: SessionHistoryEvent
  job: CompositionJobView
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

export function saveSessionStorySetup(
  sessionId: string,
  body: SaveSessionStorySetupRequest,
) {
  return postJson<SessionStorySetupResponse>(
    `/api/v1/sessions/${sessionId}/story-setup`,
    body,
  )
}

export function saveSessionAudioSettings(
  sessionId: string,
  body: SaveSessionAudioSettingsRequest,
) {
  return postJson<SessionAudioSettingsResponse>(
    `/api/v1/sessions/${sessionId}/audio-settings`,
    body,
  )
}

export function saveSessionStoryOutline(
  sessionId: string,
  body: SaveSessionStoryOutlineRequest,
) {
  return postJson<SessionStoryOutlineResponse>(
    `/api/v1/sessions/${sessionId}/story-outline`,
    body,
  )
}

export function startSessionComposition(
  sessionId: string,
  body: StartSessionCompositionRequest,
) {
  return postJson<SessionCompositionResponse>(
    `/api/v1/sessions/${sessionId}/composition/start`,
    body,
  )
}

export function pauseSessionComposition(
  sessionId: string,
  compositionJobId: string,
) {
  return postJson<SessionCompositionResponse>(
    `/api/v1/sessions/${sessionId}/composition/${compositionJobId}/pause`,
  )
}

export function resumeSessionComposition(
  sessionId: string,
  compositionJobId: string,
) {
  return postJson<SessionCompositionResponse>(
    `/api/v1/sessions/${sessionId}/composition/${compositionJobId}/resume`,
  )
}

export function cancelSessionComposition(
  sessionId: string,
  compositionJobId: string,
) {
  return postJson<SessionCompositionResponse>(
    `/api/v1/sessions/${sessionId}/composition/${compositionJobId}/cancel`,
  )
}

export function redirectSessionComposition(
  sessionId: string,
  compositionJobId: string,
  body: RedirectSessionCompositionRequest,
) {
  return postJson<SessionCompositionResponse>(
    `/api/v1/sessions/${sessionId}/composition/${compositionJobId}/redirect`,
    body,
  )
}

export function acceptSessionCompositionRewrite(
  sessionId: string,
  compositionJobId: string,
  body: AcceptRewriteSessionCompositionRequest = {},
) {
  return postJson<SessionCompositionResponse>(
    `/api/v1/sessions/${sessionId}/composition/${compositionJobId}/accept`,
    body,
  )
}

export function rejectSessionCompositionRewrite(
  sessionId: string,
  compositionJobId: string,
  body: RejectRewriteSessionCompositionRequest = {},
) {
  return postJson<SessionCompositionResponse>(
    `/api/v1/sessions/${sessionId}/composition/${compositionJobId}/reject`,
    body,
  )
}

export function selectSessionCompositionSegmentVersion(
  sessionId: string,
  segmentIndex: number,
  versionId: string,
  body: SelectCompositionSegmentVersionRequest = {},
) {
  return postJson<SessionCompositionResponse>(
    `/api/v1/sessions/${sessionId}/composition/segments/${segmentIndex}/versions/${versionId}/select`,
    body,
  )
}

export function restoreSessionPlanRevision(
  sessionId: string,
  revisionNumber: number,
  body: RestoreSessionPlanRevisionRequest,
) {
  return postJson<SessionPitchGenerationResponse>(
    `/api/v1/sessions/${sessionId}/plan-revisions/${revisionNumber}/restore`,
    body,
  )
}

export function generateSessionPitches(
  sessionId: string,
  body: GenerateSessionPitchesRequest,
) {
  return postJson<SessionPitchGenerationResponse>(
    `/api/v1/sessions/${sessionId}/pitches/generate`,
    body,
  )
}

export function generateSessionCharacterSheets(
  sessionId: string,
  body: GenerateSessionCharacterSheetsRequest,
) {
  return postJson<SessionCharacterSheetGenerationResponse>(
    `/api/v1/sessions/${sessionId}/characters/generate`,
    body,
  )
}

export function generateSessionBeatSheet(
  sessionId: string,
  body: GenerateSessionBeatSheetRequest,
) {
  return postJson<SessionBeatSheetGenerationResponse>(
    `/api/v1/sessions/${sessionId}/beats/generate`,
    body,
  )
}

export function selectSessionPitch(
  sessionId: string,
  body: SelectSessionPitchRequest,
) {
  return postJson<SessionPitchGenerationResponse>(
    `/api/v1/sessions/${sessionId}/selections/pitch`,
    body,
  )
}

export function selectSessionCharacterSheet(
  sessionId: string,
  body: SelectSessionCharacterSheetRequest,
) {
  return postJson<SessionCharacterSheetGenerationResponse>(
    `/api/v1/sessions/${sessionId}/selections/character-sheet`,
    body,
  )
}

export function selectSessionBeatSheet(
  sessionId: string,
  body: SelectSessionBeatSheetRequest,
) {
  return postJson<SessionBeatSheetGenerationResponse>(
    `/api/v1/sessions/${sessionId}/selections/beat-sheet`,
    body,
  )
}

export function refineSessionPitch(
  sessionId: string,
  body: RefineSessionPitchRequest,
) {
  return postJson<SessionPitchGenerationResponse>(
    `/api/v1/sessions/${sessionId}/pitches/refine`,
    body,
  )
}

export function refineSessionCharacterSheet(
  sessionId: string,
  body: RefineSessionCharacterSheetRequest,
) {
  return postJson<SessionCharacterSheetGenerationResponse>(
    `/api/v1/sessions/${sessionId}/characters/refine`,
    body,
  )
}

export function refineSessionBeatSheet(
  sessionId: string,
  body: RefineSessionBeatSheetRequest,
) {
  return postJson<SessionBeatSheetGenerationResponse>(
    `/api/v1/sessions/${sessionId}/beats/refine`,
    body,
  )
}

export function editSessionBeatSheet(
  sessionId: string,
  body: EditSessionBeatSheetRequest,
) {
  return postJson<SessionBeatSheetUpdateResponse>(
    `/api/v1/sessions/${sessionId}/beats/edit`,
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
