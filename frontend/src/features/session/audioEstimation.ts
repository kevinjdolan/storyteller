import type { AudioRuntimeEstimateView } from '../../api/sessions.ts'

const DURATION_ROUNDING_SECONDS = 15

type DurationRoundingMode = 'nearest' | 'down' | 'up'

function estimateDurationSeconds(
  wordCount: number,
  wordsPerMinute: number,
  playbackSpeed: number,
) {
  if (wordCount <= 0) {
    return 0
  }

  const effectiveWordsPerMinute = Math.max(wordsPerMinute * playbackSpeed, 1)
  return Math.ceil((wordCount / effectiveWordsPerMinute) * 60)
}

function roundSeconds(
  value: number,
  mode: DurationRoundingMode,
  roundingSeconds = DURATION_ROUNDING_SECONDS,
) {
  if (value <= 0) {
    return 0
  }

  const quotient = value / roundingSeconds

  if (mode === 'down') {
    return Math.max(roundingSeconds, Math.floor(quotient) * roundingSeconds)
  }

  if (mode === 'up') {
    return Math.max(roundingSeconds, Math.ceil(quotient) * roundingSeconds)
  }

  return Math.max(roundingSeconds, Math.floor(quotient + 0.5) * roundingSeconds)
}

function classifyNarrationPacing(
  assumedWordsPerMinute: number,
  minimumWordsPerMinute: number,
  maximumWordsPerMinute: number,
  playbackSpeed: number,
) {
  const effectiveWordsPerMinute = Math.max(
    1,
    Math.round(assumedWordsPerMinute * playbackSpeed),
  )

  if (effectiveWordsPerMinute < minimumWordsPerMinute) {
    return 'roomy' as const
  }
  if (effectiveWordsPerMinute > maximumWordsPerMinute) {
    return 'brisk' as const
  }
  return 'balanced' as const
}

export function deriveAudioRuntimeEstimatePreview(
  runtimeEstimate: AudioRuntimeEstimateView | null | undefined,
  playbackSpeed: number,
) {
  if (runtimeEstimate == null) {
    return null
  }

  const pauseSeconds = runtimeEstimate.total_chapter_pause_seconds
  const targetDurationSeconds = roundSeconds(
    estimateDurationSeconds(
      runtimeEstimate.estimated_word_count,
      runtimeEstimate.assumed_words_per_minute,
      playbackSpeed,
    ) + pauseSeconds,
    'nearest',
  )
  const minimumDurationSeconds = roundSeconds(
    estimateDurationSeconds(
      runtimeEstimate.estimated_word_count,
      runtimeEstimate.maximum_words_per_minute,
      playbackSpeed,
    ) + pauseSeconds,
    'down',
  )
  const maximumDurationSeconds = roundSeconds(
    estimateDurationSeconds(
      runtimeEstimate.estimated_word_count,
      runtimeEstimate.minimum_words_per_minute,
      playbackSpeed,
    ) + pauseSeconds,
    'up',
  )

  return {
    ...runtimeEstimate,
    target_duration_seconds: Math.min(
      Math.max(targetDurationSeconds, minimumDurationSeconds),
      maximumDurationSeconds,
    ),
    minimum_duration_seconds: minimumDurationSeconds,
    maximum_duration_seconds: maximumDurationSeconds,
    pacing_band: classifyNarrationPacing(
      runtimeEstimate.assumed_words_per_minute,
      runtimeEstimate.minimum_words_per_minute,
      runtimeEstimate.maximum_words_per_minute,
      playbackSpeed,
    ),
  } satisfies AudioRuntimeEstimateView
}

export function buildAudioEstimateBasisLabel(
  runtimeEstimate: AudioRuntimeEstimateView,
) {
  if (runtimeEstimate.basis_source === 'composition_segments') {
    return 'accepted draft text'
  }
  if (runtimeEstimate.basis_source === 'story_setup_target') {
    return 'story setup target'
  }
  return 'current session data'
}

export function buildAudioEstimateAssumptionsText(
  runtimeEstimate: AudioRuntimeEstimateView,
  playbackSpeed: number,
) {
  const speedLabel = `${playbackSpeed.toFixed(2)}x`
  const pacingText = `${runtimeEstimate.assumed_words_per_minute} words per minute at ${speedLabel}`
  const rangeText = `${runtimeEstimate.minimum_words_per_minute}-${runtimeEstimate.maximum_words_per_minute} words per minute`

  if (runtimeEstimate.chapter_pause_count > 0) {
    return `Assumes about ${pacingText}, usually ${rangeText}, plus ${runtimeEstimate.chapter_pause_count} short chapter pauses at roughly ${runtimeEstimate.chapter_pause_seconds} seconds each.`
  }

  return `Assumes about ${pacingText}, usually ${rangeText}, with no extra chapter-pause buffer.`
}
