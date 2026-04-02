import { useEffect, useState } from 'react'
import type {
  AudioJobView,
  AudioMusicProfileOptionView,
  AudioSettingsView,
  SessionHistoryEvent,
  SessionSnapshot,
} from '../../api/sessions.ts'
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
  StickySummaryLayout,
  SummaryPanel,
  ToggleField,
} from '../../shared/ui/workflow.tsx'
import {
  buildAudioEstimateAssumptionsText,
  buildAudioEstimateBasisLabel,
  deriveAudioRuntimeEstimatePreview,
} from './audioEstimation.ts'
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
  const audioProgressPercent = activeAudioJob?.progress_percent ?? 0
  const audioProgressLabel = buildAudioProgressLabel(activeAudioJob)
  const audioProgressHint = buildAudioProgressHint(activeAudioJob)

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
      <section className="workspace-stage-panel">
        <div className="panel-heading">
          <div>
            <p className="eyebrow">Audio stage</p>
            <h3>Shape the narration pass before the audio render starts.</h3>
            <p>
              Voice, delivery, speed, and music stay in one durable plan. The
              runtime shown here is an estimate, not a guarantee, because the
              final script and delivery still affect timing.
            </p>
          </div>

          <div className="workspace-stage-detail__badges">
            <Badge
              tone={selectedStage.status === 'completed' ? 'success' : 'brand'}
            >
              {selectedStage.status === 'completed'
                ? 'Narration approved'
                : 'Narration in planning'}
            </Badge>
            {activeAudioJob != null ? (
              <Badge tone="accent">
                {Math.round(audioProgressPercent)}% rendered
              </Badge>
            ) : null}
            {snapshot.latest_audio_asset != null ? (
              <Badge tone="success">Audio asset ready</Badge>
            ) : (
              <Badge tone="neutral">Audio asset pending</Badge>
            )}
          </div>
        </div>

        {activeAudioJob != null ? (
          <ProgressBar
            aria-label="Narration render progress"
            className="audio-stage__progress"
            hint={audioProgressHint}
            label={audioProgressLabel}
            tone="accent"
            value={audioProgressPercent}
            valueText={`${Math.round(audioProgressPercent)}% complete`}
          />
        ) : null}

        <CardGrid className="audio-stage__cards" columns={3}>
          <SummaryPanel
            description={voiceDescription}
            label="Voice"
            title={
              voiceOptions.find((option) => option.value === formState.voiceKey)
                ?.label
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
          <SummaryPanel
            description="Route preview keeps this stage addressable without mutating the durable current-step pointer."
            label="Route mapping"
            title={
              <span className="workspace-stage-detail__route">
                ?stage={selectedStage.stage}
              </span>
            }
          />
        </CardGrid>
      </section>

      <StickySummaryLayout
        className="audio-stage__layout"
        summary={
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

            {runtimeEstimate != null ? (
              <InlineHelp title="Approximate timing" tone="info">
                <p>
                  Based on the {runtimeBasisLabel}, roughly{' '}
                  {runtimeEstimate.estimated_word_count} words, and a live{' '}
                  {formState.playbackSpeed.toFixed(2)}x playback preview.
                </p>
                <p>{runtimeAssumptions}</p>
                <p>
                  Expect a {runtimeEstimate.pacing_band} delivery. Actual
                  runtime can still shift once the final narration pass is
                  rendered.
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

            {activeAudioJob != null ? (
              <InlineHelp title="Active render" tone="warning">
                <p>
                  Saving new settings updates the durable plan for the next
                  narration pass and cancels the current audio job if one is
                  still running.
                </p>
                {audioProgressHint != null ? <p>{audioProgressHint}</p> : null}
              </InlineHelp>
            ) : null}

            {snapshot.latest_audio_asset != null ? (
              <InlineHelp title="Regeneration note" tone="warning">
                <p>
                  Any saved change marks the current listening asset stale until
                  narration runs again with the new settings.
                </p>
              </InlineHelp>
            ) : null}
          </div>
        }
      >
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
      </StickySummaryLayout>
    </>
  )
}
