import { fireEvent, screen, waitFor } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import type { SessionSnapshot } from '../../api/sessions.ts'
import { renderWithAppProviders } from '../../test/renderWithAppProviders.tsx'
import type { SessionCompositionStreamState } from './sessionRuntimeStore.ts'
import { CompositionStage } from './CompositionStage.tsx'

const sampleSnapshot: SessionSnapshot = {
  id: 'moonlit-harbor',
  display_title: 'Lanterns Over Juniper Lake',
  current_stage: 'composition',
  resume_stage: 'composition',
  furthest_completed_stage: 'story_setup',
  overall_status: 'in_progress',
  created_at: '2026-04-01T03:00:00Z',
  updated_at: '2026-04-02T05:15:00Z',
  completed_at: null,
  selected_genre: {
    id: 'genre-1',
    slug: 'quest-fantasy',
    label: 'Quest Fantasy',
  },
  selected_tone_profile: {
    id: 'tone-1',
    slug: 'hushed-wonder',
    label: 'Hushed Wonder',
  },
  progress: {
    total_stages: 10,
    completed_stages: 7,
    in_progress_stages: 1,
    needs_regeneration_stages: 0,
  },
  stage_states: [
    {
      stage: 'composition',
      label: 'Composition',
      description: 'Write the story durably in segments.',
      status: 'in_progress',
      detail: 'Writing segment 2.',
    },
  ],
  story_brief: null,
  selected_pitch: null,
  selected_character_sheet: null,
  selected_beat_sheet: {
    id: 'beat-1',
    revision_number: 1,
    summary: 'A harbor arc that softens into homecoming.',
    beats: [],
    focus_beats: [],
    accepted_at: '2026-04-02T05:00:00Z',
  },
  selected_story_setup: {
    id: 'setup-1',
    revision_number: 1,
    target_word_count: 1800,
    target_runtime_minutes: 12,
    chapter_count: 3,
    approximate_scene_count: 8,
    chapter_style: 'short',
    guidance_notes: 'Let each chapter settle before the next one brightens.',
  },
  selected_story_outline: {
    id: 'outline-1',
    revision_number: 1,
    outline_kind: 'chapter',
    summary: 'Three chapters ready for drafting.',
    cards: [
      {
        card_key: 'chapter-1',
        card_type: 'chapter',
        position: 1,
        title: 'Opening harbor',
        purpose: 'Establish the harbor and the promise.',
        summary: 'Bring Mira to the first lantern.',
        beat_keys: ['opening_image'],
        beat_labels: ['Opening Image'],
        emotional_shift: 'Move from stillness to gentle motion.',
        target_word_count: 600,
        target_runtime_minutes: 4,
        target_scene_count: 3,
        tone_direction: 'Stay luminous and calm.',
        bedtime_guardrail: 'Keep the problem small and reassuring.',
        drafting_brief: 'Open the harbor and launch the first promise.',
      },
    ],
    genre_label: 'Quest Fantasy',
    tone_label: 'Hushed Wonder',
    accepted_at: '2026-04-02T05:10:00Z',
  },
  latest_composition_job: {
    id: 'composition-job-1',
    job_kind: 'composition',
    status: 'in_progress',
    progress_percent: 54,
    current_segment_id: 'segment-2',
    current_segment_index: 2,
    total_segments: 3,
    accepted_story_so_far:
      'Draft segment 1 settles the harbor.\n\nMira followed the bell toward the quieter cove.',
    latest_partial_output: 'Mira followed the bell toward the quieter cove.',
    latest_segment_summary:
      'Segment 1 settled the harbor before the cove opened.',
    updated_at: '2026-04-02T05:16:00Z',
  },
  active_composition_job: {
    id: 'composition-job-1',
    job_kind: 'composition',
    status: 'in_progress',
    progress_percent: 54,
    current_segment_id: 'segment-2',
    current_segment_index: 2,
    total_segments: 3,
    accepted_story_so_far:
      'Draft segment 1 settles the harbor.\n\nMira followed the bell toward the quieter cove.',
    latest_partial_output: 'Mira followed the bell toward the quieter cove.',
    latest_segment_summary:
      'Segment 1 settled the harbor before the cove opened.',
    updated_at: '2026-04-02T05:16:00Z',
  },
  active_audio_job: null,
  latest_story_asset: null,
  latest_audio_asset: null,
}

const liveComposition: SessionCompositionStreamState = {
  jobId: 'composition-job-1',
  status: 'in_progress',
  currentSegmentId: 'segment-2',
  currentSegmentIndex: 2,
  totalSegments: 3,
  storyText:
    'Draft segment 1 settles the harbor.\n\nMira followed the bell toward the quieter cove.',
  latestPartialOutput: 'Mira followed the bell toward the quieter cove.',
  latestSegmentSummary: 'Segment 1 settled the harbor before the cove opened.',
  lastChunkText: 'toward the quieter cove.',
  source: 'live',
  updatedAt: '2026-04-02T05:16:00Z',
}

describe('CompositionStage', () => {
  it('renders the live manuscript and routes redirect requests through the callbacks', async () => {
    const onCancelComposition = vi.fn().mockResolvedValue(undefined)
    const onPauseComposition = vi.fn().mockResolvedValue(undefined)
    const onRedirectComposition = vi.fn().mockResolvedValue(undefined)
    const onResumeComposition = vi.fn().mockResolvedValue(undefined)
    const onStartComposition = vi.fn().mockResolvedValue(undefined)

    renderWithAppProviders(
      <CompositionStage
        composition={liveComposition}
        connectionState="open"
        onCancelComposition={onCancelComposition}
        onPauseComposition={onPauseComposition}
        onRedirectComposition={onRedirectComposition}
        onResumeComposition={onResumeComposition}
        onStartComposition={onStartComposition}
        snapshot={sampleSnapshot}
      />,
    )

    expect(screen.getByText('Segment 2 / 3')).toBeInTheDocument()
    expect(screen.getByTestId('composition-manuscript')).toHaveTextContent(
      'Mira followed the bell toward the quieter cove.',
    )
    expect(screen.getByText('Live chunks')).toBeInTheDocument()

    fireEvent.click(screen.getByRole('button', { name: 'Pause writing' }))
    await waitFor(() => {
      expect(onPauseComposition).toHaveBeenCalledWith('composition-job-1')
    })

    fireEvent.change(screen.getByLabelText('Rewrite guidance'), {
      target: {
        value: 'Soften the midpoint and bring Pip into the scene earlier.',
      },
    })
    fireEvent.click(
      screen.getByRole('button', { name: 'Rewrite from current segment' }),
    )

    await waitFor(() => {
      expect(onRedirectComposition).toHaveBeenCalledWith({
        instructions: 'Soften the midpoint and bring Pip into the scene earlier.',
        rewriteFromSegmentIndex: 2,
      })
    })
    expect(onCancelComposition).not.toHaveBeenCalled()
    expect(onResumeComposition).not.toHaveBeenCalled()
    expect(onStartComposition).not.toHaveBeenCalled()
  })
})
