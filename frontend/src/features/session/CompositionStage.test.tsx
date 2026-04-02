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
      {
        card_key: 'chapter-2',
        card_type: 'chapter',
        position: 2,
        title: 'Lantern cove',
        purpose: 'Let the quieter cove feel safe and luminous.',
        summary: 'Mira follows the drifting bell into the lantern cove.',
        beat_keys: ['fun_and_games', 'midpoint'],
        beat_labels: ['Fun and Games', 'Midpoint'],
        emotional_shift: 'Move from curiosity to anchored wonder.',
        target_word_count: 580,
        target_runtime_minutes: 4,
        target_scene_count: 2,
        tone_direction: 'Keep the lanterns gentle and warm.',
        bedtime_guardrail: 'Make the discovery awe-filled instead of sharp.',
        drafting_brief:
          'Let the cove widen the wonder without raising the tension.',
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
  it('renders the current segment focus, archive, and routes control requests through the callbacks', async () => {
    const onCancelComposition = vi.fn().mockResolvedValue(undefined)
    const onPauseComposition = vi.fn().mockResolvedValue(undefined)
    const onRedirectComposition = vi.fn().mockResolvedValue(undefined)
    const onResumeComposition = vi.fn().mockResolvedValue(undefined)
    const onReturnToPlan = vi.fn().mockResolvedValue(undefined)
    const onStartComposition = vi.fn().mockResolvedValue(undefined)

    renderWithAppProviders(
      <CompositionStage
        composition={liveComposition}
        connectionState="open"
        onCancelComposition={onCancelComposition}
        onPauseComposition={onPauseComposition}
        onRedirectComposition={onRedirectComposition}
        onResumeComposition={onResumeComposition}
        onReturnToPlan={onReturnToPlan}
        onStartComposition={onStartComposition}
        snapshot={sampleSnapshot}
      />,
    )

    expect(screen.getByText('Writing segment 2 of 3')).toBeInTheDocument()
    expect(screen.getAllByText('Lantern cove')).not.toHaveLength(0)
    expect(screen.getByText('Earlier accepted manuscript')).toBeInTheDocument()
    expect(screen.getByTestId('composition-current-surface')).toHaveTextContent(
      'Mira followed the bell toward the quieter cove.',
    )
    expect(
      screen.getByTestId('composition-current-surface'),
    ).not.toHaveTextContent('Draft segment 1 settles the harbor.')
    expect(
      screen.getByTestId('composition-manuscript-archive'),
    ).toHaveTextContent('Draft segment 1 settles the harbor.')
    expect(screen.getByText('Live chunks')).toBeInTheDocument()
    expect(
      screen.getByRole('button', { name: 'Return to plan' }),
    ).toBeInTheDocument()

    fireEvent.click(screen.getByRole('button', { name: 'Pause writing' }))
    await waitFor(() => {
      expect(onPauseComposition).toHaveBeenCalledWith('composition-job-1')
    })

    fireEvent.change(screen.getByLabelText('Rewrite guidance'), {
      target: {
        value: 'Soften the midpoint and bring Pip into the scene earlier.',
      },
    })
    fireEvent.click(screen.getByRole('button', { name: 'Request rewrite' }))

    await waitFor(() => {
      expect(onRedirectComposition).toHaveBeenCalledWith({
        instructions:
          'Soften the midpoint and bring Pip into the scene earlier.',
        rewriteFromSegmentIndex: 2,
      })
    })

    fireEvent.click(screen.getByRole('button', { name: 'Return to plan' }))
    await waitFor(() => {
      expect(onReturnToPlan).toHaveBeenCalledTimes(1)
    })

    expect(onCancelComposition).not.toHaveBeenCalled()
    expect(onResumeComposition).not.toHaveBeenCalled()
    expect(onStartComposition).not.toHaveBeenCalled()
  })

  it('shows a ready-to-write state without an archive before the first segment exists', () => {
    const idleSnapshot: SessionSnapshot = {
      ...sampleSnapshot,
      latest_composition_job: null,
      active_composition_job: null,
    }
    const idleComposition: SessionCompositionStreamState = {
      jobId: null,
      status: null,
      currentSegmentId: null,
      currentSegmentIndex: null,
      totalSegments: null,
      storyText: '',
      latestPartialOutput: '',
      latestSegmentSummary: null,
      lastChunkText: null,
      source: 'none',
      updatedAt: null,
    }

    renderWithAppProviders(
      <CompositionStage
        composition={idleComposition}
        connectionState="idle"
        onCancelComposition={vi.fn().mockResolvedValue(undefined)}
        onPauseComposition={vi.fn().mockResolvedValue(undefined)}
        onRedirectComposition={vi.fn().mockResolvedValue(undefined)}
        onResumeComposition={vi.fn().mockResolvedValue(undefined)}
        onReturnToPlan={vi.fn().mockResolvedValue(undefined)}
        onStartComposition={vi.fn().mockResolvedValue(undefined)}
        snapshot={idleSnapshot}
      />,
    )

    expect(screen.getByText('Ready to write')).toBeInTheDocument()
    expect(
      screen.getByRole('button', { name: 'Start writing' }),
    ).toBeInTheDocument()
    expect(
      screen.queryByTestId('composition-manuscript-archive'),
    ).not.toBeInTheDocument()
  })

  it('surfaces queued interruption state while the worker finishes a safe checkpoint', () => {
    renderWithAppProviders(
      <CompositionStage
        composition={liveComposition}
        connectionState="open"
        onCancelComposition={vi.fn().mockResolvedValue(undefined)}
        onPauseComposition={vi.fn().mockResolvedValue(undefined)}
        onRedirectComposition={vi.fn().mockResolvedValue(undefined)}
        onResumeComposition={vi.fn().mockResolvedValue(undefined)}
        onReturnToPlan={vi.fn().mockResolvedValue(undefined)}
        onStartComposition={vi.fn().mockResolvedValue(undefined)}
        snapshot={{
          ...sampleSnapshot,
          active_composition_job: {
            ...sampleSnapshot.active_composition_job!,
            interruption_request: {
              id: 'interrupt-1',
              request_kind: 'redirect',
              state: 'requested',
              origin: 'workspace',
              message:
                'Rewrite requested from segment 2. The current chunk will finish saving before the redirect applies.',
              instructions: 'Soften the midpoint and bring Pip in sooner.',
              rewrite_from_segment_index: 2,
              requested_status: 'in_progress',
              requested_segment_id: 'segment-2',
              requested_segment_index: 2,
              requested_progress_percent: 54,
              created_at: '2026-04-02T05:16:30Z',
              updated_at: '2026-04-02T05:16:30Z',
            },
          },
          latest_composition_job: {
            ...sampleSnapshot.latest_composition_job!,
            interruption_request: {
              id: 'interrupt-1',
              request_kind: 'redirect',
              state: 'requested',
              origin: 'workspace',
              message:
                'Rewrite requested from segment 2. The current chunk will finish saving before the redirect applies.',
              instructions: 'Soften the midpoint and bring Pip in sooner.',
              rewrite_from_segment_index: 2,
              requested_status: 'in_progress',
              requested_segment_id: 'segment-2',
              requested_segment_index: 2,
              requested_progress_percent: 54,
              created_at: '2026-04-02T05:16:30Z',
              updated_at: '2026-04-02T05:16:30Z',
            },
          },
        }}
      />,
    )

    expect(screen.getAllByText('Redirect queued')).toHaveLength(2)
    expect(
      screen.getAllByText(
        'Rewrite requested from segment 2. The current chunk will finish saving before the redirect applies.',
      ),
    ).toHaveLength(2)
    expect(screen.getByRole('button', { name: 'Pause writing' })).toBeDisabled()
    expect(screen.getByRole('button', { name: 'Request rewrite' })).toBeDisabled()
  })
})
