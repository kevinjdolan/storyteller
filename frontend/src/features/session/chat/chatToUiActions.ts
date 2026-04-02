import { type WorkflowStageId, isWorkflowStageId } from '../workflowStages.ts'

export const CHAT_TO_UI_ACTION_SCHEMA_VERSION = 1

export const chatToUiActionTypes = [
  'navigate_to_stage',
  'select_genre',
  'select_tone',
  'update_story_brief',
  'regenerate_pitches',
  'refine_pitch',
  'select_pitch',
  'select_character_sheet',
  'refine_character_sheet',
  'regenerate_character_sheet',
  'accept_beat_sheet',
  'refine_beat_sheet',
  'regenerate_beat_sheet',
  'update_story_setup',
  'start_composition',
  'pause_job',
  'resume_job',
  'redirect_composition',
  'update_audio_settings',
  'start_audio_generation',
  'open_finalize_view',
  'download_asset',
] as const

export type ChatToUiActionType = (typeof chatToUiActionTypes)[number]

export const chatToUiActionDefaultPolicies = {
  navigate_to_stage: 'auto_apply_candidate',
  select_genre: 'confirm_first',
  select_tone: 'confirm_first',
  update_story_brief: 'auto_apply_candidate',
  regenerate_pitches: 'confirm_first',
  refine_pitch: 'confirm_first',
  select_pitch: 'confirm_first',
  select_character_sheet: 'confirm_first',
  refine_character_sheet: 'confirm_first',
  regenerate_character_sheet: 'confirm_first',
  accept_beat_sheet: 'confirm_first',
  refine_beat_sheet: 'confirm_first',
  regenerate_beat_sheet: 'confirm_first',
  update_story_setup: 'auto_apply_candidate',
  start_composition: 'confirm_first',
  pause_job: 'confirm_first',
  resume_job: 'confirm_first',
  redirect_composition: 'confirm_first',
  update_audio_settings: 'auto_apply_candidate',
  start_audio_generation: 'confirm_first',
  open_finalize_view: 'auto_apply_candidate',
  download_asset: 'auto_apply_candidate',
} as const satisfies Record<ChatToUiActionType, ChatToUiActionDefaultPolicy>

const jobKinds = ['composition', 'audio'] as const
const storyBriefEditModes = ['replace', 'append', 'merge'] as const
const compositionStartModes = ['fresh', 'continue', 'rewrite'] as const
const finalizeViews = ['reader', 'player'] as const
const downloadAssetKinds = ['story_docx', 'final_audio'] as const

export type ChatToUiActionDefaultPolicy =
  | 'auto_apply_candidate'
  | 'confirm_first'
export type ChatToUiJobKind = (typeof jobKinds)[number]
export type StoryBriefEditMode = (typeof storyBriefEditModes)[number]
export type CompositionStartMode = (typeof compositionStartModes)[number]
export type FinalizeView = (typeof finalizeViews)[number]
export type DownloadAssetKind = (typeof downloadAssetKinds)[number]

export type SelectGenreValues = {
  genre_id?: string | null
  genre_slug?: string | null
  genre_label?: string | null
}

export type SelectToneValues = {
  tone_profile_id?: string | null
  tone_profile_slug?: string | null
  tone_profile_label?: string | null
}

export type UpdateStoryBriefValues = {
  story_idea?: string | null
  desired_themes?: string | null
  key_images?: string | null
  audience_notes?: string | null
  must_have_elements?: string | null
  raw_brief?: string | null
  normalized_summary?: string | null
  planning_notes?: string | null
  edit_mode: StoryBriefEditMode
}

export type RegeneratePitchesValues = {
  candidate_count?: number | null
  guidance?: string | null
  preserve_selected_pitch: boolean
}

export type RefinePitchValues = {
  pitch_id?: string | null
  generation_key?: string | null
  pitch_index?: number | null
  title?: string | null
  instructions: string
}

export type SelectPitchValues = {
  pitch_id?: string | null
  generation_key?: string | null
  pitch_index?: number | null
  title?: string | null
}

export type SelectCharacterSheetValues = {
  character_sheet_id?: string | null
  revision_number?: number | null
  title?: string | null
}

export type RefineCharacterSheetValues = {
  instructions: string
  focus_character_names: string[]
  change_summary?: string | null
}

export type RegenerateCharacterSheetValues = {
  guidance?: string | null
}

export type AcceptBeatSheetValues = {
  beat_sheet_id?: string | null
  revision_number?: number | null
}

export type RefineBeatSheetValues = {
  instructions: string
  beat_names: string[]
  bedtime_goal?: string | null
}

export type RegenerateBeatSheetValues = {
  guidance?: string | null
  focus_beats: string[]
}

export type UpdateStorySetupValues = {
  target_word_count?: number | null
  target_runtime_minutes?: number | null
  chapter_count?: number | null
  chapter_style?: string | null
  guidance_notes?: string | null
}

export type StartCompositionValues = {
  mode: CompositionStartMode
  instructions?: string | null
  restart_from_segment_index?: number | null
}

export type JobControlValues = {
  job_kind: ChatToUiJobKind
  job_id?: string | null
  reason?: string | null
}

export type RedirectCompositionValues = {
  instructions: string
  rewrite_from_segment_index?: number | null
  preserve_completed_segments: boolean
}

export type UpdateAudioSettingsValues = {
  voice_key?: string | null
  playback_speed?: number | null
  include_background_music?: boolean | null
  music_profile?: string | null
  guidance_notes?: string | null
}

export type StartAudioGenerationValues = {
  voice_key?: string | null
  playback_speed?: number | null
  include_background_music?: boolean | null
  music_profile?: string | null
  regenerate_existing_audio: boolean
}

export type OpenFinalizeViewValues = {
  view: FinalizeView
}

export type DownloadAssetValues = {
  asset_kind: DownloadAssetKind
}

type ChatToUiActionBase<TActionType extends ChatToUiActionType, TValues> = {
  schema_version: typeof CHAT_TO_UI_ACTION_SCHEMA_VERSION
  action_type: TActionType
  target_stage: WorkflowStageId
  confidence: number
  rationale?: string | null
  requires_confirmation: boolean
  extracted_values: TValues
}

export type NavigateToStageAction = ChatToUiActionBase<
  'navigate_to_stage',
  Record<string, never>
>

export type SelectGenreAction = ChatToUiActionBase<
  'select_genre',
  SelectGenreValues
> & {
  target_stage: 'genre'
}

export type SelectToneAction = ChatToUiActionBase<
  'select_tone',
  SelectToneValues
> & {
  target_stage: 'tone'
}

export type UpdateStoryBriefAction = ChatToUiActionBase<
  'update_story_brief',
  UpdateStoryBriefValues
> & {
  target_stage: 'brief'
}

export type RegeneratePitchesAction = ChatToUiActionBase<
  'regenerate_pitches',
  RegeneratePitchesValues
> & {
  target_stage: 'pitches'
}

export type RefinePitchAction = ChatToUiActionBase<
  'refine_pitch',
  RefinePitchValues
> & {
  target_stage: 'pitches'
}

export type SelectPitchAction = ChatToUiActionBase<
  'select_pitch',
  SelectPitchValues
> & {
  target_stage: 'pitches'
}

export type SelectCharacterSheetAction = ChatToUiActionBase<
  'select_character_sheet',
  SelectCharacterSheetValues
> & {
  target_stage: 'characters'
}

export type RefineCharacterSheetAction = ChatToUiActionBase<
  'refine_character_sheet',
  RefineCharacterSheetValues
> & {
  target_stage: 'characters'
}

export type RegenerateCharacterSheetAction = ChatToUiActionBase<
  'regenerate_character_sheet',
  RegenerateCharacterSheetValues
> & {
  target_stage: 'characters'
}

export type AcceptBeatSheetAction = ChatToUiActionBase<
  'accept_beat_sheet',
  AcceptBeatSheetValues
> & {
  target_stage: 'beats'
}

export type RefineBeatSheetAction = ChatToUiActionBase<
  'refine_beat_sheet',
  RefineBeatSheetValues
> & {
  target_stage: 'beats'
}

export type RegenerateBeatSheetAction = ChatToUiActionBase<
  'regenerate_beat_sheet',
  RegenerateBeatSheetValues
> & {
  target_stage: 'beats'
}

export type UpdateStorySetupAction = ChatToUiActionBase<
  'update_story_setup',
  UpdateStorySetupValues
> & {
  target_stage: 'story_setup'
}

export type StartCompositionAction = ChatToUiActionBase<
  'start_composition',
  StartCompositionValues
> & {
  target_stage: 'composition'
}

export type PauseJobAction = ChatToUiActionBase<
  'pause_job',
  JobControlValues
> & {
  target_stage: 'composition' | 'audio'
}

export type ResumeJobAction = ChatToUiActionBase<
  'resume_job',
  JobControlValues
> & {
  target_stage: 'composition' | 'audio'
}

export type RedirectCompositionAction = ChatToUiActionBase<
  'redirect_composition',
  RedirectCompositionValues
> & {
  target_stage: 'composition'
}

export type UpdateAudioSettingsAction = ChatToUiActionBase<
  'update_audio_settings',
  UpdateAudioSettingsValues
> & {
  target_stage: 'audio'
}

export type StartAudioGenerationAction = ChatToUiActionBase<
  'start_audio_generation',
  StartAudioGenerationValues
> & {
  target_stage: 'audio'
}

export type OpenFinalizeViewAction = ChatToUiActionBase<
  'open_finalize_view',
  OpenFinalizeViewValues
> & {
  target_stage: 'finalize'
}

export type DownloadAssetAction = ChatToUiActionBase<
  'download_asset',
  DownloadAssetValues
> & {
  target_stage: 'finalize'
}

export type ChatToUiAction =
  | NavigateToStageAction
  | SelectGenreAction
  | SelectToneAction
  | UpdateStoryBriefAction
  | RegeneratePitchesAction
  | RefinePitchAction
  | SelectPitchAction
  | SelectCharacterSheetAction
  | RefineCharacterSheetAction
  | RegenerateCharacterSheetAction
  | AcceptBeatSheetAction
  | RefineBeatSheetAction
  | RegenerateBeatSheetAction
  | UpdateStorySetupAction
  | StartCompositionAction
  | PauseJobAction
  | ResumeJobAction
  | RedirectCompositionAction
  | UpdateAudioSettingsAction
  | StartAudioGenerationAction
  | OpenFinalizeViewAction
  | DownloadAssetAction

export type ChatToUiActionBatch = {
  schema_version: typeof CHAT_TO_UI_ACTION_SCHEMA_VERSION
  actions: ChatToUiAction[]
}

type JsonRecord = Record<string, unknown>

function isRecord(value: unknown): value is JsonRecord {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
}

function isOneOf<T extends string>(
  value: unknown,
  allowed: readonly T[],
): value is T {
  return typeof value === 'string' && allowed.includes(value as T)
}

function readRequiredString(record: JsonRecord, key: string) {
  const value = record[key]
  return typeof value === 'string' && value.length > 0 ? value : null
}

function readOptionalString(record: JsonRecord, key: string) {
  const value = record[key]

  if (value == null) {
    return null
  }

  return typeof value === 'string' && value.length > 0 ? value : null
}

function readOptionalNumber(record: JsonRecord, key: string) {
  const value = record[key]

  if (value == null) {
    return null
  }

  return typeof value === 'number' && Number.isFinite(value) ? value : null
}

function readOptionalInteger(record: JsonRecord, key: string) {
  const value = readOptionalNumber(record, key)
  return value != null && Number.isInteger(value) ? value : null
}

function readOptionalBoolean(record: JsonRecord, key: string) {
  const value = record[key]

  if (value == null) {
    return null
  }

  return typeof value === 'boolean' ? value : null
}

function readStringArray(record: JsonRecord, key: string) {
  const value = record[key]

  if (!Array.isArray(value)) {
    return null
  }

  const strings = value.filter(
    (entry): entry is string => typeof entry === 'string' && entry.length > 0,
  )

  return strings.length === value.length ? strings : null
}

function readExtractedValues(record: JsonRecord) {
  const value = record.extracted_values

  if (value == null) {
    return {}
  }

  return isRecord(value) ? value : null
}

function readStage(record: JsonRecord) {
  const value = record.target_stage
  return typeof value === 'string' && isWorkflowStageId(value) ? value : null
}

function readConfidence(record: JsonRecord) {
  const value = readOptionalNumber(record, 'confidence')
  return value != null && value >= 0 && value <= 1 ? value : null
}

type ParsedBaseAction = {
  schema_version: typeof CHAT_TO_UI_ACTION_SCHEMA_VERSION
  action_type: ChatToUiActionType
  target_stage: WorkflowStageId
  confidence: number
  rationale: string | null
  requires_confirmation: boolean
}

function parseBaseAction(record: JsonRecord): ParsedBaseAction | null {
  if (record.schema_version !== CHAT_TO_UI_ACTION_SCHEMA_VERSION) {
    return null
  }

  const actionType = isOneOf(record.action_type, chatToUiActionTypes)
    ? record.action_type
    : null
  const targetStage = readStage(record)
  const confidence = readConfidence(record)
  const requiresConfirmation = readOptionalBoolean(
    record,
    'requires_confirmation',
  )

  if (
    actionType == null ||
    targetStage == null ||
    confidence == null ||
    requiresConfirmation == null
  ) {
    return null
  }

  if (
    getChatToUiActionDefaultPolicy(actionType) === 'confirm_first' &&
    !requiresConfirmation
  ) {
    return null
  }

  return {
    schema_version: CHAT_TO_UI_ACTION_SCHEMA_VERSION,
    action_type: actionType,
    target_stage: targetStage,
    confidence,
    rationale: readOptionalString(record, 'rationale'),
    requires_confirmation: requiresConfirmation,
  }
}

function hasAnyDefined(values: Array<unknown>) {
  return values.some((value) => value != null)
}

function parseChatToUiAction(record: JsonRecord): ChatToUiAction | null {
  const base = parseBaseAction(record)

  if (base == null) {
    return null
  }

  const extractedValues = readExtractedValues(record)

  if (extractedValues == null) {
    return null
  }

  switch (base.action_type) {
    case 'navigate_to_stage':
      return {
        ...base,
        schema_version: CHAT_TO_UI_ACTION_SCHEMA_VERSION,
        action_type: 'navigate_to_stage',
        extracted_values: {},
      }

    case 'select_genre': {
      if (base.target_stage !== 'genre') {
        return null
      }

      const values: SelectGenreValues = {
        genre_id: readOptionalString(extractedValues, 'genre_id'),
        genre_slug: readOptionalString(extractedValues, 'genre_slug'),
        genre_label: readOptionalString(extractedValues, 'genre_label'),
      }

      return hasAnyDefined(Object.values(values))
        ? {
            ...base,
            schema_version: CHAT_TO_UI_ACTION_SCHEMA_VERSION,
            action_type: 'select_genre',
            target_stage: 'genre',
            extracted_values: values,
          }
        : null
    }

    case 'select_tone': {
      if (base.target_stage !== 'tone') {
        return null
      }

      const values: SelectToneValues = {
        tone_profile_id: readOptionalString(extractedValues, 'tone_profile_id'),
        tone_profile_slug: readOptionalString(
          extractedValues,
          'tone_profile_slug',
        ),
        tone_profile_label: readOptionalString(
          extractedValues,
          'tone_profile_label',
        ),
      }

      return hasAnyDefined(Object.values(values))
        ? {
            ...base,
            schema_version: CHAT_TO_UI_ACTION_SCHEMA_VERSION,
            action_type: 'select_tone',
            target_stage: 'tone',
            extracted_values: values,
          }
        : null
    }

    case 'update_story_brief': {
      if (base.target_stage !== 'brief') {
        return null
      }

      const editMode = isOneOf(extractedValues.edit_mode, storyBriefEditModes)
        ? extractedValues.edit_mode
        : 'merge'
      const values: UpdateStoryBriefValues = {
        story_idea: readOptionalString(extractedValues, 'story_idea'),
        desired_themes: readOptionalString(extractedValues, 'desired_themes'),
        key_images: readOptionalString(extractedValues, 'key_images'),
        audience_notes: readOptionalString(extractedValues, 'audience_notes'),
        must_have_elements: readOptionalString(
          extractedValues,
          'must_have_elements',
        ),
        raw_brief: readOptionalString(extractedValues, 'raw_brief'),
        normalized_summary: readOptionalString(
          extractedValues,
          'normalized_summary',
        ),
        planning_notes: readOptionalString(extractedValues, 'planning_notes'),
        edit_mode: editMode,
      }

      return hasAnyDefined([
        values.story_idea,
        values.desired_themes,
        values.key_images,
        values.audience_notes,
        values.must_have_elements,
        values.raw_brief,
        values.normalized_summary,
        values.planning_notes,
      ])
        ? {
            ...base,
            schema_version: CHAT_TO_UI_ACTION_SCHEMA_VERSION,
            action_type: 'update_story_brief',
            target_stage: 'brief',
            extracted_values: values,
          }
        : null
    }

    case 'regenerate_pitches': {
      if (base.target_stage !== 'pitches') {
        return null
      }

      const candidateCount = readOptionalInteger(
        extractedValues,
        'candidate_count',
      )
      if (
        candidateCount != null &&
        (candidateCount < 2 || candidateCount > 6)
      ) {
        return null
      }

      return {
        ...base,
        schema_version: CHAT_TO_UI_ACTION_SCHEMA_VERSION,
        action_type: 'regenerate_pitches',
        target_stage: 'pitches',
        extracted_values: {
          candidate_count: candidateCount,
          guidance: readOptionalString(extractedValues, 'guidance'),
          preserve_selected_pitch:
            readOptionalBoolean(extractedValues, 'preserve_selected_pitch') ??
            false,
        },
      }
    }

    case 'refine_pitch': {
      if (base.target_stage !== 'pitches') {
        return null
      }

      const instructions = readRequiredString(extractedValues, 'instructions')
      const values: Omit<RefinePitchValues, 'instructions'> = {
        pitch_id: readOptionalString(extractedValues, 'pitch_id'),
        generation_key: readOptionalString(extractedValues, 'generation_key'),
        pitch_index: readOptionalInteger(extractedValues, 'pitch_index'),
        title: readOptionalString(extractedValues, 'title'),
      }

      return instructions != null && hasAnyDefined(Object.values(values))
        ? {
            ...base,
            schema_version: CHAT_TO_UI_ACTION_SCHEMA_VERSION,
            action_type: 'refine_pitch',
            target_stage: 'pitches',
            extracted_values: {
              ...values,
              instructions,
            },
          }
        : null
    }

    case 'select_pitch': {
      if (base.target_stage !== 'pitches') {
        return null
      }

      const values: SelectPitchValues = {
        pitch_id: readOptionalString(extractedValues, 'pitch_id'),
        generation_key: readOptionalString(extractedValues, 'generation_key'),
        pitch_index: readOptionalInteger(extractedValues, 'pitch_index'),
        title: readOptionalString(extractedValues, 'title'),
      }

      return hasAnyDefined(Object.values(values))
        ? {
            ...base,
            schema_version: CHAT_TO_UI_ACTION_SCHEMA_VERSION,
            action_type: 'select_pitch',
            target_stage: 'pitches',
            extracted_values: values,
          }
        : null
    }

    case 'select_character_sheet': {
      if (base.target_stage !== 'characters') {
        return null
      }

      const values: SelectCharacterSheetValues = {
        character_sheet_id: readOptionalString(
          extractedValues,
          'character_sheet_id',
        ),
        revision_number: readOptionalInteger(
          extractedValues,
          'revision_number',
        ),
        title: readOptionalString(extractedValues, 'title'),
      }

      return hasAnyDefined(Object.values(values))
        ? {
            ...base,
            schema_version: CHAT_TO_UI_ACTION_SCHEMA_VERSION,
            action_type: 'select_character_sheet',
            target_stage: 'characters',
            extracted_values: values,
          }
        : null
    }

    case 'refine_character_sheet': {
      if (base.target_stage !== 'characters') {
        return null
      }

      const instructions = readRequiredString(extractedValues, 'instructions')
      const focusCharacterNames =
        readStringArray(extractedValues, 'focus_character_names') ?? []

      return instructions == null
        ? null
        : {
            ...base,
            schema_version: CHAT_TO_UI_ACTION_SCHEMA_VERSION,
            action_type: 'refine_character_sheet',
            target_stage: 'characters',
            extracted_values: {
              instructions,
              focus_character_names: focusCharacterNames,
              change_summary: readOptionalString(
                extractedValues,
                'change_summary',
              ),
            },
          }
    }

    case 'regenerate_character_sheet':
      return base.target_stage === 'characters'
        ? {
            ...base,
            schema_version: CHAT_TO_UI_ACTION_SCHEMA_VERSION,
            action_type: 'regenerate_character_sheet',
            target_stage: 'characters',
            extracted_values: {
              guidance: readOptionalString(extractedValues, 'guidance'),
            },
          }
        : null

    case 'accept_beat_sheet': {
      if (base.target_stage !== 'beats') {
        return null
      }

      const values: AcceptBeatSheetValues = {
        beat_sheet_id: readOptionalString(extractedValues, 'beat_sheet_id'),
        revision_number: readOptionalInteger(
          extractedValues,
          'revision_number',
        ),
      }

      return hasAnyDefined(Object.values(values))
        ? {
            ...base,
            schema_version: CHAT_TO_UI_ACTION_SCHEMA_VERSION,
            action_type: 'accept_beat_sheet',
            target_stage: 'beats',
            extracted_values: values,
          }
        : null
    }

    case 'refine_beat_sheet': {
      if (base.target_stage !== 'beats') {
        return null
      }

      const instructions = readRequiredString(extractedValues, 'instructions')
      const beatNames = readStringArray(extractedValues, 'beat_names') ?? []

      return instructions == null
        ? null
        : {
            ...base,
            schema_version: CHAT_TO_UI_ACTION_SCHEMA_VERSION,
            action_type: 'refine_beat_sheet',
            target_stage: 'beats',
            extracted_values: {
              instructions,
              beat_names: beatNames,
              bedtime_goal: readOptionalString(extractedValues, 'bedtime_goal'),
            },
          }
    }

    case 'regenerate_beat_sheet':
      return base.target_stage === 'beats'
        ? {
            ...base,
            schema_version: CHAT_TO_UI_ACTION_SCHEMA_VERSION,
            action_type: 'regenerate_beat_sheet',
            target_stage: 'beats',
            extracted_values: {
              guidance: readOptionalString(extractedValues, 'guidance'),
              focus_beats:
                readStringArray(extractedValues, 'focus_beats') ?? [],
            },
          }
        : null

    case 'update_story_setup': {
      if (base.target_stage !== 'story_setup') {
        return null
      }

      const targetWordCount = readOptionalInteger(
        extractedValues,
        'target_word_count',
      )
      const targetRuntimeMinutes = readOptionalInteger(
        extractedValues,
        'target_runtime_minutes',
      )
      const chapterCount = readOptionalInteger(extractedValues, 'chapter_count')

      if (
        (targetWordCount != null &&
          (targetWordCount < 100 || targetWordCount > 10000)) ||
        (targetRuntimeMinutes != null &&
          (targetRuntimeMinutes < 1 || targetRuntimeMinutes > 180)) ||
        (chapterCount != null && (chapterCount < 1 || chapterCount > 24))
      ) {
        return null
      }

      const values: UpdateStorySetupValues = {
        target_word_count: targetWordCount,
        target_runtime_minutes: targetRuntimeMinutes,
        chapter_count: chapterCount,
        chapter_style: readOptionalString(extractedValues, 'chapter_style'),
        guidance_notes: readOptionalString(extractedValues, 'guidance_notes'),
      }

      return hasAnyDefined(Object.values(values))
        ? {
            ...base,
            schema_version: CHAT_TO_UI_ACTION_SCHEMA_VERSION,
            action_type: 'update_story_setup',
            target_stage: 'story_setup',
            extracted_values: values,
          }
        : null
    }

    case 'start_composition': {
      if (base.target_stage !== 'composition') {
        return null
      }

      return {
        ...base,
        schema_version: CHAT_TO_UI_ACTION_SCHEMA_VERSION,
        action_type: 'start_composition',
        target_stage: 'composition',
        extracted_values: {
          mode: isOneOf(extractedValues.mode, compositionStartModes)
            ? extractedValues.mode
            : 'fresh',
          instructions: readOptionalString(extractedValues, 'instructions'),
          restart_from_segment_index: readOptionalInteger(
            extractedValues,
            'restart_from_segment_index',
          ),
        },
      }
    }

    case 'pause_job': {
      if (
        base.target_stage !== 'composition' &&
        base.target_stage !== 'audio'
      ) {
        return null
      }

      const jobKind = isOneOf(extractedValues.job_kind, jobKinds)
        ? extractedValues.job_kind
        : null
      if (jobKind == null || jobKind !== base.target_stage) {
        return null
      }

      return {
        ...base,
        schema_version: CHAT_TO_UI_ACTION_SCHEMA_VERSION,
        action_type: 'pause_job',
        target_stage: base.target_stage,
        extracted_values: {
          job_kind: jobKind,
          job_id: readOptionalString(extractedValues, 'job_id'),
          reason: readOptionalString(extractedValues, 'reason'),
        },
      }
    }

    case 'resume_job': {
      if (
        base.target_stage !== 'composition' &&
        base.target_stage !== 'audio'
      ) {
        return null
      }

      const jobKind = isOneOf(extractedValues.job_kind, jobKinds)
        ? extractedValues.job_kind
        : null
      if (jobKind == null || jobKind !== base.target_stage) {
        return null
      }

      return {
        ...base,
        schema_version: CHAT_TO_UI_ACTION_SCHEMA_VERSION,
        action_type: 'resume_job',
        target_stage: base.target_stage,
        extracted_values: {
          job_kind: jobKind,
          job_id: readOptionalString(extractedValues, 'job_id'),
          reason: readOptionalString(extractedValues, 'reason'),
        },
      }
    }

    case 'redirect_composition': {
      if (base.target_stage !== 'composition') {
        return null
      }

      const instructions = readRequiredString(extractedValues, 'instructions')
      return instructions == null
        ? null
        : {
            ...base,
            schema_version: CHAT_TO_UI_ACTION_SCHEMA_VERSION,
            action_type: 'redirect_composition',
            target_stage: 'composition',
            extracted_values: {
              instructions,
              rewrite_from_segment_index: readOptionalInteger(
                extractedValues,
                'rewrite_from_segment_index',
              ),
              preserve_completed_segments:
                readOptionalBoolean(
                  extractedValues,
                  'preserve_completed_segments',
                ) ?? true,
            },
          }
    }

    case 'update_audio_settings': {
      if (base.target_stage !== 'audio') {
        return null
      }

      const playbackSpeed = readOptionalNumber(
        extractedValues,
        'playback_speed',
      )
      if (
        playbackSpeed != null &&
        (playbackSpeed < 0.5 || playbackSpeed > 2.0)
      ) {
        return null
      }

      const values: UpdateAudioSettingsValues = {
        voice_key: readOptionalString(extractedValues, 'voice_key'),
        playback_speed: playbackSpeed,
        include_background_music: readOptionalBoolean(
          extractedValues,
          'include_background_music',
        ),
        music_profile: readOptionalString(extractedValues, 'music_profile'),
        guidance_notes: readOptionalString(extractedValues, 'guidance_notes'),
      }

      return hasAnyDefined(Object.values(values))
        ? {
            ...base,
            schema_version: CHAT_TO_UI_ACTION_SCHEMA_VERSION,
            action_type: 'update_audio_settings',
            target_stage: 'audio',
            extracted_values: values,
          }
        : null
    }

    case 'start_audio_generation': {
      if (base.target_stage !== 'audio') {
        return null
      }

      const playbackSpeed = readOptionalNumber(
        extractedValues,
        'playback_speed',
      )
      if (
        playbackSpeed != null &&
        (playbackSpeed < 0.5 || playbackSpeed > 2.0)
      ) {
        return null
      }

      return {
        ...base,
        schema_version: CHAT_TO_UI_ACTION_SCHEMA_VERSION,
        action_type: 'start_audio_generation',
        target_stage: 'audio',
        extracted_values: {
          voice_key: readOptionalString(extractedValues, 'voice_key'),
          playback_speed: playbackSpeed,
          include_background_music: readOptionalBoolean(
            extractedValues,
            'include_background_music',
          ),
          music_profile: readOptionalString(extractedValues, 'music_profile'),
          regenerate_existing_audio:
            readOptionalBoolean(extractedValues, 'regenerate_existing_audio') ??
            false,
        },
      }
    }

    case 'open_finalize_view': {
      if (base.target_stage !== 'finalize') {
        return null
      }

      const view = isOneOf(extractedValues.view, finalizeViews)
        ? extractedValues.view
        : null
      return view == null
        ? null
        : {
            ...base,
            schema_version: CHAT_TO_UI_ACTION_SCHEMA_VERSION,
            action_type: 'open_finalize_view',
            target_stage: 'finalize',
            extracted_values: {
              view,
            },
          }
    }

    case 'download_asset': {
      if (base.target_stage !== 'finalize') {
        return null
      }

      const assetKind = isOneOf(extractedValues.asset_kind, downloadAssetKinds)
        ? extractedValues.asset_kind
        : null
      return assetKind == null
        ? null
        : {
            ...base,
            schema_version: CHAT_TO_UI_ACTION_SCHEMA_VERSION,
            action_type: 'download_asset',
            target_stage: 'finalize',
            extracted_values: {
              asset_kind: assetKind,
            },
          }
    }
  }
}

export function getChatToUiActionDefaultPolicy(
  actionType: ChatToUiActionType,
): ChatToUiActionDefaultPolicy {
  return chatToUiActionDefaultPolicies[actionType]
}

export function parseChatToUiActionBatch(
  value: unknown,
): ChatToUiActionBatch | null {
  if (
    !isRecord(value) ||
    value.schema_version !== CHAT_TO_UI_ACTION_SCHEMA_VERSION
  ) {
    return null
  }

  if (!Array.isArray(value.actions)) {
    return null
  }

  const actions = value.actions.map((entry) =>
    isRecord(entry) ? parseChatToUiAction(entry) : null,
  )

  return actions.some((action) => action == null)
    ? null
    : {
        schema_version: CHAT_TO_UI_ACTION_SCHEMA_VERSION,
        actions: actions as ChatToUiAction[],
      }
}
