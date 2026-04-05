import { useEffect, useState } from 'react'
import type {
  AudioJobView,
  AudioMusicProfileOptionView,
  AudioSegmentView,
  AudioSettingsView,
  SessionHistoryEvent,
  SessionSnapshot,
} from '../../api/sessions.ts'
import { getButtonClassName } from '../../shared/ui/buttonStyles.ts'
import {
  Badge,
  Button,
  ProgressBar,
  TextArea,
} from '../../shared/ui/primitives.tsx'
import {
  CardGrid,
  FormColumns,
  InlineHelp,
  SelectField,
  SliderField,
  SummaryPanel,
  ToggleField,
} from '../../shared/ui/workflow.tsx'
import {
  buildAudioEstimateAssumptionsText,
  buildAudioEstimateBasisLabel,
  deriveAudioRuntimeEstimatePreview,
} from './audioEstimation.ts'
import {
  resolveSessionAssetDownloadUrl,
  resolveSessionAssetStreamUrl,
} from './sessionArtifacts.ts'
import type { SessionWorkspaceStageView } from './sessionStageScaffold.ts'

type AudioSettingsStageProps = {
  onSaveAudioSettings: (input: {
    voiceKey?: AudioSettingsView['voice_key'] | null
    narrationStyle?: AudioSettingsView['narration_style'] | null
    playbackSpeed?: number | null
    includeBackgroundMusic?: boolean | null
    musicProfile?: AudioSettingsView['music_profile'] | null
    narrationVolume?: number | null
    musicVolume?: number | null
    guidanceNotes?: string | null
    origin: string
  }) => Promise<{
    event: SessionHistoryEvent
    snapshot: SessionSnapshot
  }>
  selectedStage: SessionWorkspaceStageView
  snapshot: SessionSnapshot
}

type AudioSettingsFormState = {
  voiceKey: AudioSettingsView['voice_key']
  narrationStyle: AudioSettingsView['narration_style']
  playbackSpeed: number
  includeBackgroundMusic: boolean
  musicProfile: AudioSettingsView['music_profile']
  narrationVolume: number
  musicVolume: number
  guidanceNotes: string
}

type AudioRenderState =
  | 'planned'
  | 'queued'
  | 'generating'
  | 'mixing'
  | 'paused'
  | 'failed'
  | 'completed'

type AudioSegmentDisplayStatus =
  | 'ready'
  | 'queued'
  | 'generating'
  | 'paused'
  | 'failed'

const voiceOptions = [
  {
    value: 'moonbeam',
    label: 'Moonbeam',
    description: 'Softest and most airy for slower wind-down stories.',
  },
  {
    value: 'hearthside',
    label: 'Hearthside',
    description: 'Warm and tucked-in, good for cozy family scenes.',
  },
  {
    value: 'storykeeper',
    label: 'Storykeeper',
    description:
      'Clearer diction for longer narration passes and chapter breaks.',
  },
] as const

const narrationStyleOptions = [
  {
    value: 'calm',
    label: 'Calm',
    description: 'Even pacing with gentle phrasing and clear breath points.',
  },
  {
    value: 'hushed',
    label: 'Hushed',
    description: 'Extra-soft delivery that leans bedtime-first.',
  },
  {
    value: 'warm',
    label: 'Warm',
    description: 'Slightly more expressive while keeping the night settled.',
  },
] as const

const fallbackMusicOptions: AudioMusicProfileOptionView[] = [
  {
    key: 'lullaby_piano',
    label: 'Lullaby piano',
    description: 'Simple keys under the voice without pulling focus.',
    bedtime_use_case:
      'Softest choice for tender reassurance and tucked-in endings.',
    asset_file_name: 'lullaby_piano.wav',
    loop_duration_seconds: 24,
    recommended_music_volume: 24,
    recommended_music_volume_min: 12,
    recommended_music_volume_max: 28,
    mix_note:
      'Loops a sparse piano bed and fades out at the end of the narration.',
  },
  {
    key: 'string_drift',
    label: 'String drift',
    description: 'Long bowed textures for wonder-heavy stories.',
    bedtime_use_case:
      'Best for spacious fantasy or travel scenes that need more glow.',
    asset_file_name: 'string_drift.wav',
    loop_duration_seconds: 24,
    recommended_music_volume: 20,
    recommended_music_volume_min: 10,
    recommended_music_volume_max: 24,
    mix_note:
      'Uses a lower base gain so the texture stays behind the narration.',
  },
  {
    key: 'night_ambience',
    label: 'Night ambience',
    description: 'Low environmental bed for harbor, forest, or sky scenes.',
    bedtime_use_case:
      'Fits scene-setting passages that want a steady sense of place.',
    asset_file_name: 'night_ambience.wav',
    loop_duration_seconds: 24,
    recommended_music_volume: 18,
    recommended_music_volume_min: 8,
    recommended_music_volume_max: 22,
    mix_note:
      'Keeps the bed darkest and quietest so consonants remain easy to hear.',
  },
] satisfies AudioMusicProfileOptionView[]

function buildFormState(snapshot: SessionSnapshot): AudioSettingsFormState {
  const audioSettings = snapshot.audio_settings

  return {
    voiceKey: audioSettings?.voice_key ?? 'moonbeam',
    narrationStyle: audioSettings?.narration_style ?? 'calm',
    playbackSpeed: audioSettings?.playback_speed ?? 0.95,
    includeBackgroundMusic: audioSettings?.include_background_music ?? false,
    musicProfile: audioSettings?.music_profile ?? 'lullaby_piano',
    narrationVolume: audioSettings?.narration_volume ?? 92,
    musicVolume: audioSettings?.music_volume ?? 24,
    guidanceNotes: audioSettings?.guidance_notes ?? '',
  }
}

function normalizeText(value: string) {
  return value.trim()
}

function audioSettingsMatch(
  left: AudioSettingsFormState,
  right: AudioSettingsFormState,
) {
  return (
    left.voiceKey === right.voiceKey &&
    left.narrationStyle === right.narrationStyle &&
    left.playbackSpeed === right.playbackSpeed &&
    left.includeBackgroundMusic === right.includeBackgroundMusic &&
    left.musicProfile === right.musicProfile &&
    left.narrationVolume === right.narrationVolume &&
    left.musicVolume === right.musicVolume &&
    normalizeText(left.guidanceNotes) === normalizeText(right.guidanceNotes)
  )
}

function formatMinutesRange(
  runtimeEstimate: AudioSettingsView['runtime_estimate'],
) {
  if (runtimeEstimate == null) {
    return null
  }

  const targetMinutes = Math.max(
    1,
    Math.round(runtimeEstimate.target_duration_seconds / 60),
  )
  const minimumMinutes = Math.max(
    1,
    Math.round(runtimeEstimate.minimum_duration_seconds / 60),
  )
  const maximumMinutes = Math.max(
    minimumMinutes,
    Math.round(runtimeEstimate.maximum_duration_seconds / 60),
  )

  return {
    label: `Approx. ${targetMinutes} min`,
    detail: `Usually ${minimumMinutes}-${maximumMinutes} min`,
  }
}

function getSelectedOptionDescription<
  TValue extends string,
  TOption extends {
    label: string
    description: string
  },
>(options: ReadonlyArray<TOption>, value: TValue) {
  return (
    options.find((option) => {
      const optionValue =
        'value' in option ? option.value : 'key' in option ? option.key : null
      return optionValue === value
    })?.description ?? null
  )
}

function buildAudioProgressLabel(audioJob: AudioJobView | null) {
  if (audioJob?.current_step != null && audioJob.current_step.length > 0) {
    return audioJob.current_step
  }

  if (audioJob?.status != null) {
    return `Narration ${audioJob.status.replace(/_/g, ' ')}`
  }

  return 'Narration runtime'
}

function roundProgressForAnnouncement(value: number) {
  return Math.max(0, Math.min(100, Math.round(value / 10) * 10))
}

function buildAudioProgressAnnouncement(options: {
  audioJob: AudioJobView | null
  finalAudioReady: boolean
  renderState: AudioRenderState
}) {
  if (options.finalAudioReady) {
    return 'Narration complete. The final master is ready.'
  }

  if (options.renderState === 'failed') {
    return 'Narration stopped before the final master was ready.'
  }

  if (options.renderState === 'paused') {
    return 'Narration is paused with its checkpoints preserved.'
  }

  if (options.audioJob == null) {
    return 'Narration has not started yet.'
  }

  const roundedProgress = roundProgressForAnnouncement(
    options.audioJob.progress_percent ?? 0,
  )
  const stepLabel =
    options.audioJob.current_step_index != null &&
    options.audioJob.total_steps != null
      ? `Step ${options.audioJob.current_step_index} of ${options.audioJob.total_steps}.`
      : options.audioJob.current_segment_index != null &&
          options.audioJob.total_segments != null
        ? `Segment ${options.audioJob.current_segment_index} of ${options.audioJob.total_segments}.`
        : null

  return [stepLabel, `${roundedProgress}% complete.`].filter(Boolean).join(' ')
}

function buildAudioProgressHint(audioJob: AudioJobView | null) {
  if (audioJob == null) {
    return null
  }

  const stepSummary =
    audioJob.current_step_index != null && audioJob.total_steps != null
      ? `Step ${audioJob.current_step_index} of ${audioJob.total_steps}.`
      : audioJob.current_segment_index != null &&
          audioJob.total_segments != null
        ? `Segment ${audioJob.current_segment_index} of ${audioJob.total_segments}.`
        : null
  const completedSummary =
    audioJob.completed_segments != null && audioJob.total_segments != null
      ? `${audioJob.completed_segments} of ${audioJob.total_segments} narration segments are durable already.`
      : null
  const durationSummary =
    audioJob.estimated_duration_seconds != null
      ? `Estimated listening length ${Math.max(Math.round(audioJob.estimated_duration_seconds / 60), 1)} min.`
      : null

  return [stepSummary, completedSummary, durationSummary]
    .filter(Boolean)
    .join(' ')
}

function resolveAudioRenderState(
  audioJob: AudioJobView | null,
): AudioRenderState {
  if (audioJob == null) {
    return 'planned'
  }

  if (audioJob.status === 'completed') {
    return 'completed'
  }

  if (audioJob.status === 'failed' || audioJob.status === 'cancelled') {
    return 'failed'
  }

  if (audioJob.status === 'paused') {
    return 'paused'
  }

  if (audioJob.status === 'queued') {
    return 'queued'
  }

  const currentStep = audioJob.current_step?.toLowerCase() ?? ''
  const allNarrationSegmentsRendered =
    audioJob.total_segments != null &&
    audioJob.completed_segments != null &&
    audioJob.total_segments > 0 &&
    audioJob.completed_segments >= audioJob.total_segments

  if (
    currentStep.includes('mix') ||
    currentStep.includes('publish') ||
    currentStep.includes('assemble') ||
    allNarrationSegmentsRendered
  ) {
    return 'mixing'
  }

  return 'generating'
}

function getAudioRenderBadgeTone(renderState: AudioRenderState) {
  if (renderState === 'completed') {
    return 'success'
  }

  if (renderState === 'failed') {
    return 'danger'
  }

  if (renderState === 'paused') {
    return 'warning'
  }

  if (renderState === 'mixing' || renderState === 'generating') {
    return 'accent'
  }

  if (renderState === 'queued') {
    return 'brand'
  }

  return 'neutral'
}

function getAudioProgressTone(renderState: AudioRenderState) {
  if (renderState === 'completed') {
    return 'moss'
  }

  if (renderState === 'mixing' || renderState === 'generating') {
    return 'accent'
  }

  return 'brand'
}

function getAudioStatusLabel(renderState: AudioRenderState) {
  switch (renderState) {
    case 'queued':
      return 'Queued'
    case 'generating':
      return 'Generating'
    case 'mixing':
      return 'Mixing'
    case 'paused':
      return 'Paused'
    case 'failed':
      return 'Needs attention'
    case 'completed':
      return 'Done'
    default:
      return 'Planned'
  }
}

function buildAudioHeroTitle(options: {
  audioJob: AudioJobView | null
  finalAudioReady: boolean
  renderState: AudioRenderState
}) {
  const { audioJob, finalAudioReady, renderState } = options

  if (renderState === 'queued') {
    return 'Narration queued and ready for the worker.'
  }

  if (renderState === 'generating') {
    return 'Narration is rendering segment by segment.'
  }

  if (renderState === 'mixing') {
    return 'Narration segments are rendered and the final master is assembling.'
  }

  if (renderState === 'paused') {
    return 'Narration is paused with the current checkpoint preserved.'
  }

  if (renderState === 'failed') {
    return 'Narration stopped and needs another pass.'
  }

  if (renderState === 'completed' || finalAudioReady) {
    return 'Narration master is ready for a spot-check and final listen.'
  }

  if (audioJob != null) {
    return 'Narration progress is ready to follow here.'
  }

  return 'Narration progress will appear here once audio generation starts.'
}

function buildAudioHeroDescription(options: {
  audioJob: AudioJobView | null
  finalAudioReady: boolean
  previewCount: number
}) {
  const { audioJob, finalAudioReady, previewCount } = options

  if (audioJob?.current_step != null && audioJob.current_step.length > 0) {
    return audioJob.current_step
  }

  if (finalAudioReady) {
    return 'Ready preview clips stay separate from the merged narration master so spot-checks never pretend to be the final file.'
  }

  if (previewCount > 0) {
    return `${previewCount} checkpoint preview${previewCount === 1 ? ' clip is' : ' clips are'} already durable while the rest of the narration pipeline catches up.`
  }

  return 'This stage tracks durable narration checkpoints, remaining render work, and any preview clips that are ready before the final compiled file lands.'
}

function formatAudioCalloutValue(
  audioJob: AudioJobView | null,
  renderState: AudioRenderState,
  finalAudioReady: boolean,
) {
  if (audioJob != null) {
    if (renderState === 'completed') {
      return '100%'
    }

    if (audioJob.progress_percent != null) {
      return `${Math.round(audioJob.progress_percent)}%`
    }
  }

  if (finalAudioReady) {
    return 'Ready'
  }

  return 'Plan'
}

function formatCountLabel(
  count: number,
  singular: string,
  plural = `${singular}s`,
) {
  return `${count} ${count === 1 ? singular : plural}`
}

function buildRemainingWorkSummary(options: {
  audioJob: AudioJobView | null
  audioSegments: AudioSegmentView[]
  finalAudioReady: boolean
  previewCount: number
  renderState: AudioRenderState
}) {
  const {
    audioJob,
    audioSegments,
    finalAudioReady,
    previewCount,
    renderState,
  } = options
  const totalSegments = audioSegments.length || audioJob?.total_segments || 0
  const completedSegments =
    audioJob?.completed_segments ??
    audioSegments.filter((segment) => segment.status === 'completed').length
  const remainingSegments = Math.max(totalSegments - completedSegments, 0)

  if (renderState === 'completed' || (finalAudioReady && audioJob == null)) {
    return {
      title: 'No remaining render work',
      description:
        'All planned narration segments are durable, and the merged narration master is ready to review.',
    }
  }

  if (renderState === 'failed') {
    return {
      title: 'Render stopped',
      description:
        audioJob?.error_message ??
        audioJob?.stop_reason ??
        'The narration pipeline needs another pass before the compiled master can be trusted.',
    }
  }

  if (renderState === 'mixing') {
    return {
      title: 'Final assembly underway',
      description:
        previewCount > 0
          ? 'Checkpoint previews are ready. The worker is now assembling, mixing, and publishing the final narration master.'
          : 'All narration segments are rendered. The worker is now assembling and publishing the final narration master.',
    }
  }

  if (renderState === 'paused') {
    return {
      title: 'Resume to finish the queue',
      description:
        totalSegments > 0
          ? `${formatCountLabel(completedSegments, 'segment')} complete and ${formatCountLabel(remainingSegments, 'segment')} still pending.`
          : 'The current narration checkpoint is preserved until the worker resumes.',
    }
  }

  if (renderState === 'queued') {
    return {
      title: 'Worker still needs to begin',
      description:
        totalSegments > 0
          ? `${formatCountLabel(totalSegments, 'segment')} are queued for synthesis before final assembly begins.`
          : 'The narration run is queued and waiting for the worker to claim it.',
    }
  }

  if (renderState === 'generating') {
    return {
      title:
        remainingSegments > 0
          ? `${formatCountLabel(remainingSegments, 'segment')} still to render`
          : 'Waiting for the next checkpoint',
      description:
        previewCount > 0
          ? `${formatCountLabel(previewCount, 'preview clip')} already ready while the remaining segments render.`
          : 'Checkpoint previews will appear here as each narration segment finishes.',
    }
  }

  return {
    title: 'Waiting for the first render',
    description:
      'Once narration starts, this stage will show which segments are pending, currently rendering, previewable, or blocked.',
  }
}

function resolveAudioSegmentDisplayStatus(
  segment: AudioSegmentView,
  audioJob: AudioJobView | null,
) {
  if (segment.status === 'completed') {
    return 'ready'
  }

  if (segment.status === 'failed' || segment.status === 'cancelled') {
    return 'failed'
  }

  const isActiveSegment =
    audioJob?.current_segment_index === segment.segment_index &&
    (audioJob.status === 'queued' ||
      audioJob.status === 'in_progress' ||
      audioJob.status === 'paused')

  if (isActiveSegment) {
    if (audioJob.status === 'paused') {
      return 'paused'
    }

    if (audioJob.status === 'queued') {
      return 'queued'
    }

    if (resolveAudioRenderState(audioJob) === 'generating') {
      return 'generating'
    }
  }

  if (segment.status === 'in_progress') {
    return 'generating'
  }

  if (segment.status === 'paused') {
    return 'paused'
  }

  return 'queued'
}

function getAudioSegmentBadgeTone(status: AudioSegmentDisplayStatus) {
  if (status === 'ready') {
    return 'success'
  }

  if (status === 'failed') {
    return 'danger'
  }

  if (status === 'paused') {
    return 'warning'
  }

  if (status === 'generating') {
    return 'accent'
  }

  return 'neutral'
}

function getAudioSegmentStatusLabel(status: AudioSegmentDisplayStatus) {
  switch (status) {
    case 'ready':
      return 'Ready for preview'
    case 'generating':
      return 'Generating now'
    case 'paused':
      return 'Paused'
    case 'failed':
      return 'Failed'
    default:
      return 'Pending'
  }
}

function humanizeToken(value: string | null | undefined) {
  if (value == null || value.length === 0) {
    return null
  }

  return value.replace(/_/g, ' ')
}

function buildAudioSegmentMeta(segment: AudioSegmentView) {
  const metadata = [`${segment.word_count} words`]
  const splitReason = humanizeToken(segment.split_reason)
  const pauseHint = humanizeToken(segment.pause_hint)

  if (segment.pause_after_seconds > 0) {
    metadata.push(`${segment.pause_after_seconds}s pause after`)
  } else if (pauseHint != null && pauseHint !== 'none') {
    metadata.push(pauseHint)
  }

  if (splitReason != null) {
    metadata.push(splitReason)
  }

  return metadata
}

function buildSegmentPreviewCopy(
  segment: AudioSegmentView,
  displayStatus: AudioSegmentDisplayStatus,
) {
  if (resolveSessionAssetStreamUrl(segment.preview_asset) != null) {
    return 'Checkpoint preview clip'
  }

  if (segment.preview_asset != null) {
    return 'Checkpoint clip saved'
  }

  if (displayStatus === 'ready') {
    return 'Preview clip syncing'
  }

  return null
}

function readDetailsRecord(value: unknown): Record<string, unknown> | null {
  return value != null && typeof value === 'object' && !Array.isArray(value)
    ? (value as Record<string, unknown>)
    : null
}

function readNestedRecord(
  value: Record<string, unknown> | null | undefined,
  key: string,
) {
  return readDetailsRecord(value?.[key])
}

function readOptionalString(
  value: Record<string, unknown> | null | undefined,
  key: string,
) {
  const rawValue = value?.[key]
  return typeof rawValue === 'string' && rawValue.trim().length > 0
    ? rawValue.trim()
    : null
}

function formatDurationLabel(value: number | null | undefined) {
  if (value == null || !Number.isFinite(value) || value <= 0) {
    return null
  }

  const roundedSeconds = Math.round(value)
  const minutes = Math.floor(roundedSeconds / 60)
  const seconds = roundedSeconds % 60

  if (minutes <= 0) {
    return `${seconds}s`
  }

  return `${minutes}m ${seconds.toString().padStart(2, '0')}s`
}

function formatPublishedAtLabel(value: string | null | undefined) {
  if (value == null) {
    return null
  }

  const parsedValue = new Date(value)
  if (Number.isNaN(parsedValue.getTime())) {
    return null
  }

  return parsedValue.toLocaleString('en-US', {
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
    month: 'short',
  })
}

function buildCompiledAudioMeta(asset: SessionSnapshot['latest_audio_asset']) {
  if (asset == null) {
    return []
  }

  const details = readDetailsRecord(asset.details)
  const generation = readNestedRecord(details, 'generation')
  const mix = readNestedRecord(details, 'mix')
  const metadata: string[] = []
  const runtimeLabel = formatDurationLabel(asset.duration_seconds)
  if (runtimeLabel != null) {
    metadata.push(`Runtime ${runtimeLabel}`)
  }

  const voiceName = readOptionalString(generation, 'voice_name')
  const voiceKey = readOptionalString(generation, 'voice_key')
  const resolvedVoiceLabel = voiceName ?? humanizeToken(voiceKey)
  if (resolvedVoiceLabel != null) {
    metadata.push(`Voice ${resolvedVoiceLabel}`)
  }

  const mixApplied = mix?.applied
  if (mixApplied === true) {
    metadata.push('Music mixed')
  } else if (mixApplied === false) {
    metadata.push('Voice only')
  }

  const publishedAtLabel = formatPublishedAtLabel(asset.ready_at)
  if (publishedAtLabel != null) {
    metadata.push(`Published ${publishedAtLabel}`)
  }

  return metadata
}

export function AudioSettingsStage({
  onSaveAudioSettings,
  selectedStage,
  snapshot,
}: AudioSettingsStageProps) {
  const [formState, setFormState] = useState<AudioSettingsFormState>(() =>
    buildFormState(snapshot),
  )
  const [isSaving, setIsSaving] = useState(false)
  const [saveError, setSaveError] = useState<string | null>(null)

  const savedState = buildFormState(snapshot)
  const isLocked = selectedStage.availability === 'locked'
  const isDirty = !audioSettingsMatch(formState, savedState)
  const musicOptions =
    snapshot.audio_settings?.music_profile_options ?? fallbackMusicOptions
  const persistedRuntimeEstimate = snapshot.audio_settings?.runtime_estimate
  const persistedMixPreview = snapshot.audio_settings?.mix_preview
  const runtimeEstimate = deriveAudioRuntimeEstimatePreview(
    persistedRuntimeEstimate,
    formState.playbackSpeed,
  )
  const runtimeSummary = formatMinutesRange(runtimeEstimate)
  const runtimeBasisLabel =
    runtimeEstimate != null
      ? buildAudioEstimateBasisLabel(runtimeEstimate)
      : null
  const runtimeAssumptions =
    runtimeEstimate != null
      ? buildAudioEstimateAssumptionsText(
          runtimeEstimate,
          formState.playbackSpeed,
        )
      : null
  const voiceDescription = getSelectedOptionDescription(
    voiceOptions,
    formState.voiceKey,
  )
  const narrationStyleDescription = getSelectedOptionDescription(
    narrationStyleOptions,
    formState.narrationStyle,
  )
  const musicDescription = getSelectedOptionDescription(
    musicOptions,
    formState.musicProfile,
  )
  const selectedMusicOption =
    musicOptions.find((option) => option.key === formState.musicProfile) ?? null
  const isPersistedMixPreviewCurrent =
    formState.includeBackgroundMusic === savedState.includeBackgroundMusic &&
    formState.musicProfile === savedState.musicProfile &&
    formState.musicVolume === savedState.musicVolume &&
    formState.narrationVolume === savedState.narrationVolume
  const activeAudioJob = snapshot.active_audio_job ?? null
  const displayAudioJob = activeAudioJob ?? snapshot.latest_audio_job ?? null
  const renderState = resolveAudioRenderState(displayAudioJob)
  const audioSegments = snapshot.audio_segments ?? []
  const previewReadyCount = audioSegments.filter(
    (segment) => segment.preview_asset != null,
  ).length
  const previewPlayableCount = audioSegments.filter(
    (segment) => resolveSessionAssetStreamUrl(segment.preview_asset) != null,
  ).length
  const finalAudioReady = snapshot.latest_audio_asset != null
  const compiledAudioMeta = buildCompiledAudioMeta(snapshot.latest_audio_asset)
  const compiledAudioStreamUrl = resolveSessionAssetStreamUrl(
    snapshot.latest_audio_asset,
  )
  const compiledAudioDownloadUrl = resolveSessionAssetDownloadUrl(
    snapshot.latest_audio_asset,
  )
  const showingPreviousMaster =
    activeAudioJob != null &&
    snapshot.latest_audio_asset?.audio_job_id != null &&
    snapshot.latest_audio_asset.audio_job_id !== activeAudioJob.id
  const audioProgressPercent =
    displayAudioJob?.progress_percent ?? (finalAudioReady ? 100 : 0)
  const announcedAudioProgressPercent =
    roundProgressForAnnouncement(audioProgressPercent)
  const audioProgressLabel = buildAudioProgressLabel(displayAudioJob)
  const audioProgressHint = buildAudioProgressHint(displayAudioJob)
  const audioProgressAnnouncement = buildAudioProgressAnnouncement({
    audioJob: displayAudioJob,
    finalAudioReady,
    renderState,
  })
  const audioProgressAnnouncementKey = [
    displayAudioJob?.id ?? 'no-job',
    renderState,
    displayAudioJob?.current_step_index ?? 'no-step',
    displayAudioJob?.current_segment_index ?? 'no-segment',
    announcedAudioProgressPercent,
    finalAudioReady ? 'ready' : 'pending',
  ].join(':')
  const remainingWorkSummary = buildRemainingWorkSummary({
    audioJob: displayAudioJob,
    audioSegments,
    finalAudioReady,
    previewCount: previewReadyCount,
    renderState,
  })

  useEffect(() => {
    setFormState(buildFormState(snapshot))
    setSaveError(null)
  }, [snapshot])

  async function handleSave() {
    if (isLocked || !isDirty || isSaving) {
      return
    }

    setIsSaving(true)
    setSaveError(null)

    try {
      await onSaveAudioSettings({
        voiceKey: formState.voiceKey,
        narrationStyle: formState.narrationStyle,
        playbackSpeed: formState.playbackSpeed,
        includeBackgroundMusic: formState.includeBackgroundMusic,
        musicProfile: formState.musicProfile,
        narrationVolume: formState.narrationVolume,
        musicVolume: formState.musicVolume,
        guidanceNotes: normalizeText(formState.guidanceNotes) || null,
        origin: 'workspace',
      })
    } catch (error) {
      setSaveError(
        error instanceof Error
          ? error.message
          : 'Audio settings could not be saved right now.',
      )
    } finally {
      setIsSaving(false)
    }
  }

  return (
    <>
      <section
        aria-label="Audio stage runtime"
        className="workspace-stage-panel composition-stage__hero audio-stage__hero"
      >
        <div className="composition-stage__hero-header">
          <div className="composition-stage__hero-copy">
            <p className="eyebrow">Audio runtime</p>
            <h3>
              {buildAudioHeroTitle({
                audioJob: displayAudioJob,
                finalAudioReady,
                renderState,
              })}
            </h3>
            <p>
              {buildAudioHeroDescription({
                audioJob: displayAudioJob,
                finalAudioReady,
                previewCount: previewReadyCount,
              })}
            </p>
          </div>

          <div className="composition-stage__progress-callout">
            <strong>
              {formatAudioCalloutValue(
                displayAudioJob,
                renderState,
                finalAudioReady,
              )}
            </strong>
            <span>{getAudioStatusLabel(renderState)}</span>
          </div>
        </div>

        <ProgressBar
          aria-label="Narration render progress"
          announcementKey={audioProgressAnnouncementKey}
          announcementText={audioProgressAnnouncement}
          className="composition-stage__progress audio-stage__progress"
          hint={
            audioProgressHint ??
            'Checkpoint previews and the final narration master are both durable and refresh-safe.'
          }
          label={
            displayAudioJob != null ? audioProgressLabel : 'Narration progress'
          }
          tone={getAudioProgressTone(renderState)}
          value={audioProgressPercent}
          valueText={
            displayAudioJob != null || finalAudioReady
              ? `${Math.round(audioProgressPercent)}% complete`
              : 'Waiting to start'
          }
        />

        <CardGrid className="workspace-stage-detail__cards" columns={3}>
          <SummaryPanel
            description={
              displayAudioJob?.status != null
                ? `Current durable job status: ${displayAudioJob.status.replace(/_/g, ' ')}.`
                : 'No narration job is running yet, but the durable audio plan is ready.'
            }
            label="Stage status"
            title={getAudioStatusLabel(renderState)}
            tone={
              renderState === 'completed'
                ? 'accent'
                : renderState === 'failed'
                  ? 'default'
                  : 'default'
            }
          />
          <SummaryPanel
            description={remainingWorkSummary.description}
            label="Remaining work"
            title={remainingWorkSummary.title}
          />
          <SummaryPanel
            description={
              audioSegments.length > 0
                ? `${formatCountLabel(previewPlayableCount, 'clip')} can play inline right now.`
                : 'Checkpoint clips will appear here as each narration segment becomes durable.'
            }
            label="Segment previews"
            title={
              audioSegments.length > 0
                ? `${previewReadyCount}/${audioSegments.length} ready`
                : 'Not started'
            }
          />
          <SummaryPanel
            description={
              finalAudioReady
                ? 'The merged narration master stays distinct from the per-segment preview clips.'
                : 'The compiled narration file only appears after segment synthesis and final assembly both finish.'
            }
            label="Compiled file"
            title={finalAudioReady ? 'Ready to review' : 'Pending master'}
          />
        </CardGrid>
      </section>

      <div className="audio-stage__layout">
        <section className="workspace-stage-panel audio-stage__status-panel">
          <div className="panel-heading">
            <div>
              <h3>Segment status</h3>
              <p>
                Each narration segment keeps its own durable status so you can
                tell what is still pending, what is rendering now, and which
                clips are already ready for spot-checking.
              </p>
            </div>

            <div className="workspace-stage-detail__badges">
              <Badge tone={getAudioRenderBadgeTone(renderState)}>
                {getAudioStatusLabel(renderState)}
              </Badge>
              <Badge tone={previewReadyCount > 0 ? 'success' : 'neutral'}>
                {previewReadyCount > 0
                  ? `${previewReadyCount} preview${previewReadyCount === 1 ? '' : 's'} ready`
                  : 'No previews yet'}
              </Badge>
              <Badge tone={finalAudioReady ? 'success' : 'neutral'}>
                {finalAudioReady ? 'Master ready' : 'Master pending'}
              </Badge>
            </div>
          </div>

          {audioSegments.length > 0 ? (
            <ol className="audio-stage__segment-list">
              {audioSegments.map((segment) => {
                const displayStatus = resolveAudioSegmentDisplayStatus(
                  segment,
                  activeAudioJob,
                )
                const previewCopy = buildSegmentPreviewCopy(
                  segment,
                  displayStatus,
                )
                const previewAudioUrl = resolveSessionAssetStreamUrl(
                  segment.preview_asset,
                )

                return (
                  <li className="audio-stage__segment-item" key={segment.id}>
                    <div className="audio-stage__segment-copy">
                      <div className="audio-stage__segment-header">
                        <div>
                          <p className="audio-stage__segment-kicker">
                            Segment {segment.segment_index}
                          </p>
                          <h4>
                            {segment.source_outline_card_title ??
                              `Narration ${segment.segment_index}`}
                          </h4>
                        </div>
                        <Badge tone={getAudioSegmentBadgeTone(displayStatus)}>
                          {getAudioSegmentStatusLabel(displayStatus)}
                        </Badge>
                      </div>

                      <p className="audio-stage__segment-preview">
                        {segment.text_preview ??
                          'This segment is waiting for its first durable checkpoint.'}
                      </p>

                      <div className="audio-stage__segment-meta">
                        {buildAudioSegmentMeta(segment).map((item) => (
                          <span key={`${segment.id}-${item}`}>{item}</span>
                        ))}
                      </div>

                      {segment.error_message != null ? (
                        <p className="field__error" role="alert">
                          {segment.error_message}
                        </p>
                      ) : null}
                    </div>

                    <div className="audio-stage__segment-preview-panel">
                      {previewCopy != null ? (
                        <span className="audio-stage__segment-preview-label">
                          {previewCopy}
                        </span>
                      ) : null}

                      {previewAudioUrl != null ? (
                        <audio
                          aria-label={`Segment ${segment.segment_index} preview audio`}
                          className="audio-stage__player"
                          controls
                          preload="none"
                          src={previewAudioUrl}
                        />
                      ) : (
                        <p className="audio-stage__segment-preview-empty">
                          {displayStatus === 'ready'
                            ? 'Preview clip is recorded and syncing into the review surface.'
                            : 'Preview clip will appear here after this segment finishes rendering.'}
                        </p>
                      )}
                    </div>
                  </li>
                )
              })}
            </ol>
          ) : (
            <div className="audio-stage__empty">
              <p>
                Narration segments will appear here after the next audio run is
                queued from the accepted story text.
              </p>
            </div>
          )}
        </section>

        <div className="audio-stage__summary">
          <SummaryPanel
            description={narrationStyleDescription}
            label="Narration style"
            title={
              narrationStyleOptions.find(
                (option) => option.value === formState.narrationStyle,
              )?.label
            }
            tone="accent"
          />

          <SummaryPanel
            description="Route preview keeps this stage addressable without mutating the durable current-step pointer."
            label="Route mapping"
            title={
              <span className="workspace-stage-detail__route">
                ?stage={selectedStage.stage}
              </span>
            }
          />

          {runtimeEstimate != null ? (
            <InlineHelp title="Approximate timing" tone="info">
              <p>
                Based on the {runtimeBasisLabel}, roughly{' '}
                {runtimeEstimate.estimated_word_count} words, and a live{' '}
                {formState.playbackSpeed.toFixed(2)}x playback preview.
              </p>
              <p>{runtimeAssumptions}</p>
              <p>
                Expect a {runtimeEstimate.pacing_band} delivery. Actual runtime
                can still shift once the final narration pass is rendered.
              </p>
            </InlineHelp>
          ) : (
            <InlineHelp title="Estimate pending" tone="info">
              <p>
                The runtime card stays approximate by design and will sharpen
                once the story text or target word count is available.
              </p>
            </InlineHelp>
          )}

          {formState.includeBackgroundMusic && selectedMusicOption != null ? (
            <InlineHelp title="Music mix" tone="info">
              <p>{selectedMusicOption.bedtime_use_case}</p>
              <p>
                {selectedMusicOption.mix_note} Recommended bed level:{' '}
                {selectedMusicOption.recommended_music_volume_min}-
                {selectedMusicOption.recommended_music_volume_max}%.
              </p>
              {isPersistedMixPreviewCurrent && persistedMixPreview != null ? (
                <p>{persistedMixPreview.summary}</p>
              ) : null}
            </InlineHelp>
          ) : null}

          <InlineHelp title="Preview vs. master" tone="info">
            <p>
              Segment previews are checkpoint renders for spot-checking voice,
              pacing, and mix choices before the full narration master is
              assembled.
            </p>
            <p>
              The compiled file below is the merged narration output and should
              be treated as the trustable final listen.
            </p>
          </InlineHelp>

          {displayAudioJob != null ? (
            <InlineHelp title="Active render" tone="warning">
              <p>
                Saving new settings updates the durable plan for the next
                narration pass and cancels the current audio job if one is still
                running.
              </p>
              {audioProgressHint != null ? <p>{audioProgressHint}</p> : null}
            </InlineHelp>
          ) : null}

          {snapshot.latest_audio_asset != null ? (
            <section className="workspace-stage-panel audio-stage__compiled-panel">
              <div className="panel-heading">
                <div>
                  <h3>Compiled narration</h3>
                  <p>
                    This player represents the merged narration master, not an
                    individual checkpoint clip.
                  </p>
                </div>
                <Badge tone="success">Final audio</Badge>
              </div>

              {compiledAudioStreamUrl != null ? (
                <audio
                  aria-label="Compiled narration preview"
                  className="audio-stage__player"
                  controls
                  preload="none"
                  src={compiledAudioStreamUrl}
                />
              ) : (
                <p className="audio-stage__compiled-note">
                  The final narration file is ready in durable storage, but
                  inline playback is unavailable in this environment.
                </p>
              )}

              {showingPreviousMaster ? (
                <p className="audio-stage__compiled-note">
                  This player is showing the previous published master while the
                  current narration run assembles a replacement. The older file
                  stays available until the new publish succeeds.
                </p>
              ) : null}

              {compiledAudioMeta.length > 0 ? (
                <div className="audio-stage__compiled-meta">
                  {compiledAudioMeta.map((item) => (
                    <span key={item}>{item}</span>
                  ))}
                </div>
              ) : null}

              {compiledAudioDownloadUrl != null ? (
                <div className="audio-stage__compiled-actions">
                  <a
                    className={getButtonClassName({
                      size: 'compact',
                      tone: 'secondary',
                    })}
                    download
                    href={compiledAudioDownloadUrl}
                  >
                    Download narration
                  </a>
                </div>
              ) : null}
            </section>
          ) : null}
        </div>

        <section className="workspace-stage-panel audio-stage__form-panel">
          <div className="panel-heading">
            <div>
              <h3>Settings</h3>
              <p>
                Keep the first pass tight: choose the voice, shape the delivery,
                decide whether music belongs underneath it, and leave any final
                mix note for the next render.
              </p>
            </div>
          </div>

          <CardGrid className="audio-stage__cards" columns={3}>
            <SummaryPanel
              description={voiceDescription}
              label="Voice"
              title={
                voiceOptions.find(
                  (option) => option.value === formState.voiceKey,
                )?.label
              }
            />
            <SummaryPanel
              description={
                formState.includeBackgroundMusic
                  ? musicDescription
                  : 'The narration will render dry, with no background bed under the voice.'
              }
              label="Music"
              title={
                formState.includeBackgroundMusic
                  ? (selectedMusicOption?.label ?? 'Music on')
                  : 'Music off'
              }
            />
            <SummaryPanel
              description={
                runtimeSummary != null
                  ? `${runtimeSummary.detail}. Approximate preview based on ${runtimeBasisLabel}.`
                  : 'A runtime range will appear once story setup targets or accepted story text are available.'
              }
              label="Runtime estimate"
              title={runtimeSummary?.label ?? 'Approximate estimate pending'}
            />
          </CardGrid>

          <FormColumns className="audio-stage__fields">
            <SelectField
              description="Voice choice affects the default color and articulation of the narration."
              disabled={isLocked}
              label="Narration voice"
              onChange={(event) => {
                const nextValue = event.currentTarget
                  .value as AudioSettingsFormState['voiceKey']
                setFormState((current) => ({
                  ...current,
                  voiceKey: nextValue,
                }))
              }}
              options={voiceOptions.map((option) => ({
                label: option.label,
                value: option.value,
              }))}
              value={formState.voiceKey}
            />

            <SelectField
              description="Narration style shapes warmth and softness without changing the story text."
              disabled={isLocked}
              label="Narration style"
              onChange={(event) => {
                const nextValue = event.currentTarget
                  .value as AudioSettingsFormState['narrationStyle']
                setFormState((current) => ({
                  ...current,
                  narrationStyle: nextValue,
                }))
              }}
              options={narrationStyleOptions.map((option) => ({
                label: option.label,
                value: option.value,
              }))}
              value={formState.narrationStyle}
            />

            <SliderField
              description="Speed nudges the delivery slower or faster without promising an exact final runtime."
              disabled={isLocked}
              label="Playback speed"
              max={1.15}
              min={0.8}
              onChange={(event) => {
                const nextValue = Number(event.currentTarget.value)
                setFormState((current) => ({
                  ...current,
                  playbackSpeed: nextValue,
                }))
              }}
              step={0.05}
              value={formState.playbackSpeed}
              valueText={`${formState.playbackSpeed.toFixed(2)}x`}
            />

            <SliderField
              description="Keep narration comfortably forward even when music is enabled."
              disabled={isLocked}
              label="Narration volume"
              max={100}
              min={60}
              onChange={(event) => {
                const nextValue = Number(event.currentTarget.value)
                setFormState((current) => ({
                  ...current,
                  narrationVolume: nextValue,
                }))
              }}
              step={1}
              value={formState.narrationVolume}
              valueText={`${formState.narrationVolume}%`}
            />

            <ToggleField
              checked={formState.includeBackgroundMusic}
              description="Background music stays optional and should stay clearly beneath the spoken voice."
              disabled={isLocked}
              label="Background music"
              onChange={(event) => {
                const nextValue = event.currentTarget.checked
                setFormState((current) => ({
                  ...current,
                  includeBackgroundMusic: nextValue,
                }))
              }}
              stateLabel={
                formState.includeBackgroundMusic
                  ? 'Music will render underneath narration.'
                  : 'Narration will render without a background bed.'
              }
            />

            <SelectField
              description="Choose the music bed that best matches the current story lane."
              disabled={isLocked || !formState.includeBackgroundMusic}
              label="Music style"
              onChange={(event) => {
                const nextValue = event.currentTarget
                  .value as AudioSettingsFormState['musicProfile']
                setFormState((current) => ({
                  ...current,
                  musicProfile: nextValue,
                }))
              }}
              options={musicOptions.map((option) => ({
                label: option.label,
                value: option.key,
              }))}
              value={formState.musicProfile}
            />

            <SliderField
              description="Keep the music subordinate enough that consonants and comfort cues stay easy to hear."
              disabled={isLocked || !formState.includeBackgroundMusic}
              label="Music volume"
              max={40}
              min={0}
              onChange={(event) => {
                const nextValue = Number(event.currentTarget.value)
                setFormState((current) => ({
                  ...current,
                  musicVolume: nextValue,
                }))
              }}
              step={1}
              value={formState.musicVolume}
              valueText={`${formState.musicVolume}%`}
            />
          </FormColumns>

          <TextArea
            description="Use one compact note for anything the sliders cannot express, such as extra softness on dialogue or cleaner chapter pauses."
            disabled={isLocked}
            error={saveError}
            label="Mix and delivery note"
            onChange={(event) => {
              const nextValue = event.currentTarget.value
              setFormState((current) => ({
                ...current,
                guidanceNotes: nextValue,
              }))
            }}
            rows={5}
            value={formState.guidanceNotes}
          />

          <div className="cta-row audio-stage__actions">
            <Button
              disabled={isLocked || !isDirty || isSaving}
              onClick={() => {
                void handleSave()
              }}
              tone="primary"
            >
              {isSaving ? 'Saving audio settings...' : 'Save audio settings'}
            </Button>
            <Button
              disabled={isLocked || !isDirty || isSaving}
              onClick={() => {
                setFormState(savedState)
                setSaveError(null)
              }}
              tone="ghost"
            >
              Reset
            </Button>
          </div>
        </section>
      </div>
    </>
  )
}
