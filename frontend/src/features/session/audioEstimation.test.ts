import { describe, expect, it } from 'vitest'
import type { AudioRuntimeEstimateView } from '../../api/sessions.ts'
import {
  buildAudioEstimateAssumptionsText,
  buildAudioEstimateBasisLabel,
  deriveAudioRuntimeEstimatePreview,
} from './audioEstimation.ts'

const baseEstimate: AudioRuntimeEstimateView = {
  estimated_word_count: 1800,
  estimated_chapter_count: 3,
  chapter_pause_count: 2,
  chapter_pause_seconds: 3,
  total_chapter_pause_seconds: 6,
  assumed_words_per_minute: 140,
  minimum_words_per_minute: 120,
  maximum_words_per_minute: 160,
  target_duration_seconds: 825,
  minimum_duration_seconds: 705,
  maximum_duration_seconds: 960,
  basis_source: 'story_setup_target',
  pacing_band: 'balanced',
}

describe('audioEstimation', () => {
  it('recalculates the runtime preview when playback speed changes', () => {
    expect(deriveAudioRuntimeEstimatePreview(baseEstimate, 0.95)).toEqual(
      baseEstimate,
    )

    expect(deriveAudioRuntimeEstimatePreview(baseEstimate, 0.85)).toEqual({
      ...baseEstimate,
      target_duration_seconds: 915,
      minimum_duration_seconds: 795,
      maximum_duration_seconds: 1065,
      pacing_band: 'roomy',
    })
  })

  it('builds transparent basis and assumption copy', () => {
    expect(buildAudioEstimateBasisLabel(baseEstimate)).toBe('story setup target')
    expect(buildAudioEstimateAssumptionsText(baseEstimate, 0.95)).toContain(
      '140 words per minute at 0.95x',
    )
    expect(buildAudioEstimateAssumptionsText(baseEstimate, 0.95)).toContain(
      '2 short chapter pauses',
    )
  })
})
