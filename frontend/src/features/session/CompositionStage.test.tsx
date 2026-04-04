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
  composition_segments: [
    {
      segment_index: 1,
      outline_card_title: 'Opening harbor',
      outline_card_summary: 'Bring Mira to the first lantern.',
      current_version_id: 'segment-1-rev-1',
      current_revision_number: 1,
      is_stale: false,
      versions: [
        {
          id: 'segment-1-rev-1',
          composition_job_id: 'composition-job-0',
          job_kind: 'draft',
          segment_index: 1,
          revision_number: 1,
          status: 'completed',
          acceptance_state: 'accepted',
          is_current: true,
          is_stale: false,
          accepted_summary: 'Draft segment 1 settles the harbor.',
          text_content: 'Draft segment 1 settles the harbor.',
          word_count: 6,
          created_at: '2026-04-02T05:05:00Z',
          updated_at: '2026-04-02T05:06:00Z',
          completed_at: '2026-04-02T05:06:00Z',
        },
      ],
    },
    {
      segment_index: 2,
      outline_card_title: 'Lantern cove',
      outline_card_summary:
        'Mira follows the drifting bell into the lantern cove.',
      current_version_id: 'segment-2-rev-1',
      current_revision_number: 1,
      is_stale: false,
      versions: [
        {
          id: 'segment-2-rev-1',
          composition_job_id: 'composition-job-1',
          job_kind: 'draft',
          segment_index: 2,
          revision_number: 1,
          status: 'completed',
          acceptance_state: 'accepted',
          is_current: true,
          is_stale: false,
          accepted_summary:
            'Segment 1 settled the harbor before the cove opened.',
          text_content: 'Mira followed the bell toward the quieter cove.',
          word_count: 9,
          created_at: '2026-04-02T05:14:00Z',
          updated_at: '2026-04-02T05:16:00Z',
          completed_at: '2026-04-02T05:16:00Z',
        },
      ],
    },
  ],
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
    const onAcceptRewrite = vi.fn().mockResolvedValue(undefined)
    const onCancelComposition = vi.fn().mockResolvedValue(undefined)
    const onKeepExploringRewrite = vi.fn()
    const onPauseComposition = vi.fn().mockResolvedValue(undefined)
    const onRejectRewrite = vi.fn().mockResolvedValue(undefined)
    const onRedirectComposition = vi.fn().mockResolvedValue(undefined)
    const onResumeComposition = vi.fn().mockResolvedValue(undefined)
    const onRestoreSegmentVersion = vi.fn().mockResolvedValue(undefined)
    const onReturnToPlan = vi.fn().mockResolvedValue(undefined)
    const onStartComposition = vi.fn().mockResolvedValue(undefined)

    renderWithAppProviders(
      <CompositionStage
        composition={liveComposition}
        connectionState="open"
        onAcceptRewrite={onAcceptRewrite}
        onCancelComposition={onCancelComposition}
        onKeepExploringRewrite={onKeepExploringRewrite}
        onPauseComposition={onPauseComposition}
        onRejectRewrite={onRejectRewrite}
        onRedirectComposition={onRedirectComposition}
        onResumeComposition={onResumeComposition}
        onRestoreSegmentVersion={onRestoreSegmentVersion}
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
    fireEvent.click(screen.getByRole('button', { name: 'Queue rewrite' }))

    await waitFor(() => {
      expect(onRedirectComposition).toHaveBeenCalledWith({
        instructions:
          'Soften the midpoint and bring Pip into the scene earlier.',
        rewriteFromSegmentIndex: 2,
        rewriteToSegmentIndex: 2,
        downstreamRegenerationMode: null,
      })
    })

    fireEvent.click(screen.getByRole('button', { name: 'Return to plan' }))
    await waitFor(() => {
      expect(onReturnToPlan).toHaveBeenCalledTimes(1)
    })

    expect(onCancelComposition).not.toHaveBeenCalled()
    expect(onAcceptRewrite).not.toHaveBeenCalled()
    expect(onKeepExploringRewrite).not.toHaveBeenCalled()
    expect(onResumeComposition).not.toHaveBeenCalled()
    expect(onRejectRewrite).not.toHaveBeenCalled()
    expect(onRestoreSegmentVersion).not.toHaveBeenCalled()
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
        onAcceptRewrite={vi.fn().mockResolvedValue(undefined)}
        onCancelComposition={vi.fn().mockResolvedValue(undefined)}
        onKeepExploringRewrite={vi.fn()}
        onPauseComposition={vi.fn().mockResolvedValue(undefined)}
        onRejectRewrite={vi.fn().mockResolvedValue(undefined)}
        onRedirectComposition={vi.fn().mockResolvedValue(undefined)}
        onResumeComposition={vi.fn().mockResolvedValue(undefined)}
        onRestoreSegmentVersion={vi.fn().mockResolvedValue(undefined)}
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

  it('renders provider retry messaging when the worker is backing off', () => {
    const retryMessage =
      'Gemini hit a temporary rate limit while drafting segment 2 of 3. Retrying in 2s (attempt 2 of 3).'

    renderWithAppProviders(
      <CompositionStage
        composition={liveComposition}
        connectionState="open"
        onAcceptRewrite={vi.fn().mockResolvedValue(undefined)}
        onCancelComposition={vi.fn().mockResolvedValue(undefined)}
        onKeepExploringRewrite={vi.fn()}
        onPauseComposition={vi.fn().mockResolvedValue(undefined)}
        onRejectRewrite={vi.fn().mockResolvedValue(undefined)}
        onRedirectComposition={vi.fn().mockResolvedValue(undefined)}
        onResumeComposition={vi.fn().mockResolvedValue(undefined)}
        onRestoreSegmentVersion={vi.fn().mockResolvedValue(undefined)}
        onReturnToPlan={vi.fn().mockResolvedValue(undefined)}
        onStartComposition={vi.fn().mockResolvedValue(undefined)}
        snapshot={{
          ...sampleSnapshot,
          active_composition_job: {
            ...sampleSnapshot.active_composition_job!,
            status_message: retryMessage,
          },
          latest_composition_job: {
            ...sampleSnapshot.latest_composition_job!,
            status_message: retryMessage,
          },
        }}
      />,
    )

    expect(screen.getAllByText(retryMessage)).not.toHaveLength(0)
  })

  it('surfaces queued interruption state while the worker finishes a safe checkpoint', () => {
    renderWithAppProviders(
      <CompositionStage
        composition={liveComposition}
        connectionState="open"
        onAcceptRewrite={vi.fn().mockResolvedValue(undefined)}
        onCancelComposition={vi.fn().mockResolvedValue(undefined)}
        onKeepExploringRewrite={vi.fn()}
        onPauseComposition={vi.fn().mockResolvedValue(undefined)}
        onRejectRewrite={vi.fn().mockResolvedValue(undefined)}
        onRedirectComposition={vi.fn().mockResolvedValue(undefined)}
        onResumeComposition={vi.fn().mockResolvedValue(undefined)}
        onRestoreSegmentVersion={vi.fn().mockResolvedValue(undefined)}
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
    expect(screen.getByRole('button', { name: 'Queue rewrite' })).toBeDisabled()
  })

  it('shows pending rewrite comparisons and lets the user accept them', async () => {
    const onAcceptRewrite = vi.fn().mockResolvedValue(undefined)
    const onKeepExploringRewrite = vi.fn()
    const onRejectRewrite = vi.fn().mockResolvedValue(undefined)

    renderWithAppProviders(
      <CompositionStage
        composition={liveComposition}
        connectionState="open"
        onAcceptRewrite={onAcceptRewrite}
        onCancelComposition={vi.fn().mockResolvedValue(undefined)}
        onKeepExploringRewrite={onKeepExploringRewrite}
        onPauseComposition={vi.fn().mockResolvedValue(undefined)}
        onRejectRewrite={onRejectRewrite}
        onRedirectComposition={vi.fn().mockResolvedValue(undefined)}
        onResumeComposition={vi.fn().mockResolvedValue(undefined)}
        onRestoreSegmentVersion={vi.fn().mockResolvedValue(undefined)}
        onReturnToPlan={vi.fn().mockResolvedValue(undefined)}
        onStartComposition={vi.fn().mockResolvedValue(undefined)}
        snapshot={{
          ...sampleSnapshot,
          latest_composition_job: {
            ...sampleSnapshot.latest_composition_job!,
            id: 'rewrite-job-7',
            job_kind: 'rewrite',
            status: 'completed',
            pending_review: true,
            start_segment_index: 1,
            rewrite_to_segment_index: 2,
            rewrite_candidate_segment_indexes: [1, 2],
          },
          active_composition_job: null,
          composition_segments: [
            {
              ...sampleSnapshot.composition_segments![0],
              pending_version_id: 'segment-1-rev-2',
              pending_revision_number: 2,
              versions: [
                {
                  id: 'segment-1-rev-2',
                  composition_job_id: 'rewrite-job-7',
                  job_kind: 'rewrite',
                  segment_index: 1,
                  revision_number: 2,
                  status: 'completed',
                  acceptance_state: 'pending',
                  is_current: false,
                  is_stale: false,
                  accepted_summary: 'The harbor opens more gently.',
                  text_content: 'Rewrite segment 1 opens the harbor more gently.',
                  word_count: 8,
                  created_at: '2026-04-02T05:20:00Z',
                  updated_at: '2026-04-02T05:22:00Z',
                  completed_at: '2026-04-02T05:22:00Z',
                },
                ...sampleSnapshot.composition_segments![0].versions,
              ],
            },
            sampleSnapshot.composition_segments![1],
          ],
        }}
      />,
    )

    expect(screen.getAllByText('Pending rewrite').length).toBeGreaterThan(0)
    expect(screen.getAllByText('Current manuscript').length).toBeGreaterThan(0)
    expect(screen.getAllByText('Changed').length).toBeGreaterThan(0)
    expect(screen.getByText('Candidate rewrite')).toBeInTheDocument()
    expect(screen.getAllByText('Rev 02 · Pending').length).toBeGreaterThan(0)

    fireEvent.click(screen.getByRole('button', { name: 'Accept rewrite' }))

    await waitFor(() => {
      expect(onAcceptRewrite).toHaveBeenCalledWith('rewrite-job-7')
    })

    fireEvent.click(screen.getByRole('button', { name: 'Keep current draft' }))
    await waitFor(() => {
      expect(onRejectRewrite).toHaveBeenCalledWith('rewrite-job-7')
    })

    fireEvent.click(screen.getByRole('button', { name: 'Try another rewrite' }))
    expect(onKeepExploringRewrite).toHaveBeenCalledWith(1)
  })

  it('lets the user compare and restore an older accepted revision', async () => {
    const onRestoreSegmentVersion = vi.fn().mockResolvedValue(undefined)

    renderWithAppProviders(
      <CompositionStage
        composition={liveComposition}
        connectionState="open"
        onAcceptRewrite={vi.fn().mockResolvedValue(undefined)}
        onCancelComposition={vi.fn().mockResolvedValue(undefined)}
        onKeepExploringRewrite={vi.fn()}
        onPauseComposition={vi.fn().mockResolvedValue(undefined)}
        onRejectRewrite={vi.fn().mockResolvedValue(undefined)}
        onRedirectComposition={vi.fn().mockResolvedValue(undefined)}
        onResumeComposition={vi.fn().mockResolvedValue(undefined)}
        onRestoreSegmentVersion={onRestoreSegmentVersion}
        onReturnToPlan={vi.fn().mockResolvedValue(undefined)}
        onStartComposition={vi.fn().mockResolvedValue(undefined)}
        snapshot={{
          ...sampleSnapshot,
          composition_segments: [
            {
              ...sampleSnapshot.composition_segments![1],
              versions: [
                sampleSnapshot.composition_segments![1].versions[0],
                {
                  id: 'segment-2-rev-0',
                  composition_job_id: 'composition-job-0',
                  job_kind: 'draft',
                  segment_index: 2,
                  revision_number: 0,
                  status: 'completed',
                  acceptance_state: 'accepted',
                  is_current: false,
                  is_stale: false,
                  accepted_summary: 'The earlier cove draft kept the bell closer.',
                  text_content:
                    'Mira followed the bell into the lantern cove while Pip hummed beside her.',
                  word_count: 13,
                  created_at: '2026-04-02T05:10:00Z',
                  updated_at: '2026-04-02T05:11:00Z',
                  completed_at: '2026-04-02T05:11:00Z',
                },
              ],
            },
          ],
        }}
      />,
    )

    expect(screen.getByText('Selected revision')).toBeInTheDocument()

    fireEvent.click(screen.getByRole('button', { name: 'Restore this revision' }))

    await waitFor(() => {
      expect(onRestoreSegmentVersion).toHaveBeenCalledWith(
        2,
        'segment-2-rev-0',
      )
    })
  })
})
