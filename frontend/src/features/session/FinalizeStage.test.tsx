import { fireEvent, screen, waitFor } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import type { SessionSnapshot } from '../../api/sessions.ts'
import { renderWithAppProviders } from '../../test/renderWithAppProviders.tsx'
import { FinalizeStage } from './FinalizeStage.tsx'

const baseSnapshot: SessionSnapshot = {
  id: 'session-finalize-1',
  display_title: 'Lanterns Over Juniper Lake',
  working_title: 'Lanterns Over Juniper Lake',
  current_stage: 'finalize',
  resume_stage: 'finalize',
  furthest_completed_stage: 'audio',
  overall_status: 'completed',
  created_at: '2026-04-01T03:00:00Z',
  updated_at: '2026-04-02T05:30:00Z',
  completed_at: '2026-04-02T05:30:00Z',
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
    completed_stages: 10,
    in_progress_stages: 0,
    needs_regeneration_stages: 0,
  },
  stage_states: [
    {
      stage: 'finalize',
      label: 'Finalize',
      description: 'Read, listen, review final assets, and download exports.',
      status: 'completed',
      detail: 'Everything is ready for final review.',
    },
  ],
  pitch_batches: [],
  character_sheet_batches: [],
  beat_sheet_revisions: [],
  story_outline_revisions: [],
  plan_revisions: [],
  selected_story_setup: {
    id: 'setup-1',
    revision_number: 1,
    target_word_count: 1800,
    target_runtime_minutes: 12,
    chapter_count: 3,
    approximate_scene_count: 8,
    chapter_style: 'short',
    guidance_notes: 'Keep the pacing gentle enough for bedtime.',
  },
  latest_composition_job: {
    id: 'rewrite-job-4',
    job_kind: 'rewrite',
    status: 'completed',
    progress_percent: 100,
    current_segment_index: 2,
    rewrite_to_segment_index: 2,
    pending_review: true,
    rewrite_candidate_segment_indexes: [2],
    accepted_story_so_far:
      'Draft segment 1 settles the harbor.\n\nDraft segment 2 keeps the bell close.',
    updated_at: '2026-04-02T05:30:00Z',
  },
  latest_audio_job: null,
  active_composition_job: null,
  active_audio_job: null,
  composition_segments: [
    {
      segment_index: 2,
      outline_card_title: 'Lantern cove',
      outline_card_summary: 'Mira follows the bell into the cove.',
      current_version_id: 'segment-2-rev-1',
      current_revision_number: 1,
      pending_version_id: 'segment-2-rev-2',
      pending_revision_number: 2,
      is_stale: false,
      versions: [
        {
          id: 'segment-2-rev-2',
          composition_job_id: 'rewrite-job-4',
          job_kind: 'rewrite',
          segment_index: 2,
          revision_number: 2,
          status: 'completed',
          acceptance_state: 'pending',
          is_current: false,
          is_stale: false,
          accepted_summary: 'The rewrite softens the cove entrance.',
          text_content: 'Rewrite segment 2 opens the cove more gently.',
          word_count: 8,
          created_at: '2026-04-02T05:25:00Z',
          updated_at: '2026-04-02T05:30:00Z',
          completed_at: '2026-04-02T05:30:00Z',
        },
        {
          id: 'segment-2-rev-1',
          composition_job_id: 'draft-job-1',
          job_kind: 'draft',
          segment_index: 2,
          revision_number: 1,
          status: 'completed',
          acceptance_state: 'accepted',
          is_current: true,
          is_stale: false,
          accepted_summary: 'The current draft keeps the bell close.',
          text_content: 'Draft segment 2 keeps the bell close.',
          word_count: 7,
          created_at: '2026-04-02T05:20:00Z',
          updated_at: '2026-04-02T05:22:00Z',
          completed_at: '2026-04-02T05:22:00Z',
        },
      ],
    },
  ],
  audio_segments: [],
  latest_story_asset: null,
  latest_audio_asset: null,
  audio_settings: {
    voice_key: 'moonbeam',
    narration_style: 'calm',
    playback_speed: 0.95,
    include_background_music: false,
    music_profile: 'lullaby_piano',
    narration_volume: 92,
    music_volume: 24,
    guidance_notes: '',
  },
}

function buildSnapshot(
  overrides: Partial<SessionSnapshot> = {},
): SessionSnapshot {
  return {
    ...baseSnapshot,
    ...overrides,
  }
}

afterEach(() => {
  vi.restoreAllMocks()
  vi.unstubAllGlobals()
})

describe('FinalizeStage', () => {
  it('keeps rewrite compare controls available from final review', async () => {
    const onAcceptRewrite = vi.fn().mockResolvedValue(undefined)
    const onDownloadAudio = vi.fn()
    const onDownloadStoryExport = vi.fn()
    const onRejectRewrite = vi.fn().mockResolvedValue(undefined)
    const onRestoreSegmentVersion = vi.fn().mockResolvedValue(undefined)
    const onReturnToComposition = vi.fn()

    renderWithAppProviders(
      <FinalizeStage
        onAcceptRewrite={onAcceptRewrite}
        onDownloadAudio={onDownloadAudio}
        onDownloadStoryExport={onDownloadStoryExport}
        onKeepExploringRewrite={vi.fn()}
        onRejectRewrite={onRejectRewrite}
        onRestoreSegmentVersion={onRestoreSegmentVersion}
        onReturnToComposition={onReturnToComposition}
        snapshot={buildSnapshot()}
      />,
    )

    expect(screen.getByText('Revision compare')).toBeInTheDocument()
    expect(screen.getAllByText('Changed').length).toBeGreaterThan(0)

    fireEvent.click(screen.getByRole('button', { name: 'Accept rewrite' }))
    await waitFor(() => {
      expect(onAcceptRewrite).toHaveBeenCalledWith('rewrite-job-4')
    })

    fireEvent.click(screen.getByRole('button', { name: 'Keep current draft' }))
    await waitFor(() => {
      expect(onRejectRewrite).toHaveBeenCalledWith('rewrite-job-4')
    })

    fireEvent.click(
      screen.getByRole('button', { name: 'Return to composition' }),
    )
    expect(onReturnToComposition).toHaveBeenCalledTimes(1)
    expect(onDownloadAudio).not.toHaveBeenCalled()
    expect(onDownloadStoryExport).not.toHaveBeenCalled()
    expect(onRestoreSegmentVersion).not.toHaveBeenCalled()
  })

  it('renders calm read and listen surfaces once finalized assets exist', async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      new Response('# Chapter 1\n\nMira carried the lantern home.', {
        status: 200,
        headers: {
          'Content-Type': 'text/markdown; charset=utf-8',
        },
      }),
    )
    vi.stubGlobal('fetch', fetchMock)

    const onDownloadAudio = vi.fn()
    const onDownloadStoryExport = vi.fn()

    renderWithAppProviders(
      <FinalizeStage
        onAcceptRewrite={vi.fn().mockResolvedValue(undefined)}
        onDownloadAudio={onDownloadAudio}
        onDownloadStoryExport={onDownloadStoryExport}
        onKeepExploringRewrite={vi.fn()}
        onRejectRewrite={vi.fn().mockResolvedValue(undefined)}
        onRestoreSegmentVersion={vi.fn().mockResolvedValue(undefined)}
        onReturnToComposition={vi.fn()}
        snapshot={buildSnapshot({
          latest_composition_job: {
            ...baseSnapshot.latest_composition_job!,
            pending_review: false,
          },
          latest_story_asset: {
            id: 'story-asset-1',
            asset_kind: 'story_text',
            status: 'ready',
            access: {
              download_path:
                '/api/v1/sessions/session-finalize-1/assets/story-asset-1/content?disposition=attachment',
              filename: 'lanterns-over-juniper-lake.md',
              stream_path:
                '/api/v1/sessions/session-finalize-1/assets/story-asset-1/content?disposition=inline',
            },
            public_url:
              '/api/v1/sessions/session-finalize-1/assets/story-asset-1/content?disposition=inline',
            details: {
              word_count: 1782,
            },
            ready_at: '2026-04-02T05:28:00Z',
          },
          latest_audio_asset: {
            id: 'audio-asset-1',
            asset_kind: 'final_audio',
            status: 'ready',
            access: {
              download_path:
                '/api/v1/sessions/session-finalize-1/assets/audio-asset-1/content?disposition=attachment',
              filename: 'lanterns-over-juniper-lake.mp3',
              stream_path:
                '/api/v1/sessions/session-finalize-1/assets/audio-asset-1/content?disposition=inline',
            },
            public_url:
              '/api/v1/sessions/session-finalize-1/assets/audio-asset-1/content?disposition=inline',
            duration_seconds: 734,
            details: {
              generation: {
                voice_key: 'moonbeam',
                voice_name: 'Moonbeam',
              },
              mix: {
                applied: true,
              },
            },
            ready_at: '2026-04-02T05:29:00Z',
          },
          latest_audio_job: {
            id: 'audio-job-1',
            status: 'completed',
            progress_percent: 100,
            current_step: 'Narration published',
            attempt_count: 1,
            created_at: '2026-04-02T05:20:00Z',
            updated_at: '2026-04-02T05:29:00Z',
          },
        })}
      />,
    )

    expect(
      await screen.findByRole('heading', { name: 'Chapter 1' }),
    ).toBeInTheDocument()
    expect(screen.getByText('Quest Fantasy')).toBeInTheDocument()
    expect(
      screen.getByText('1,800 words • ~12 min • 3 chapters'),
    ).toBeInTheDocument()

    fireEvent.click(
      screen.getByRole('button', { name: 'Download Word document' }),
    )
    expect(onDownloadStoryExport).toHaveBeenCalledTimes(1)

    fireEvent.click(screen.getByRole('tab', { name: 'Listen back' }))
    expect(screen.getByLabelText('Final narration preview')).toBeInTheDocument()

    fireEvent.click(
      screen.getByRole('button', { name: 'Download narration master' }),
    )
    expect(onDownloadAudio).toHaveBeenCalledTimes(1)
  })

  it('keeps the story readable while narration is still processing', async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      new Response('# Chapter 1\n\nMira carried the lantern home.', {
        status: 200,
      }),
    )
    vi.stubGlobal('fetch', fetchMock)

    renderWithAppProviders(
      <FinalizeStage
        onAcceptRewrite={vi.fn().mockResolvedValue(undefined)}
        onDownloadAudio={vi.fn()}
        onDownloadStoryExport={vi.fn()}
        onKeepExploringRewrite={vi.fn()}
        onRejectRewrite={vi.fn().mockResolvedValue(undefined)}
        onRestoreSegmentVersion={vi.fn().mockResolvedValue(undefined)}
        onReturnToComposition={vi.fn()}
        snapshot={buildSnapshot({
          latest_composition_job: {
            ...baseSnapshot.latest_composition_job!,
            pending_review: false,
          },
          latest_story_asset: {
            id: 'story-asset-2',
            asset_kind: 'story_text',
            status: 'ready',
            access: {
              download_path:
                '/api/v1/sessions/session-finalize-1/assets/story-asset-2/content?disposition=attachment',
              filename: 'lanterns-over-juniper-lake.md',
              stream_path:
                '/api/v1/sessions/session-finalize-1/assets/story-asset-2/content?disposition=inline',
            },
            public_url:
              '/api/v1/sessions/session-finalize-1/assets/story-asset-2/content?disposition=inline',
            ready_at: '2026-04-02T05:28:00Z',
          },
          latest_audio_asset: null,
          active_audio_job: {
            id: 'audio-job-2',
            status: 'in_progress',
            progress_percent: 64,
            current_step: 'Rendering segment 3 of 5',
            completed_segments: 3,
            total_segments: 5,
            current_segment_index: 3,
            attempt_count: 1,
            created_at: '2026-04-02T05:24:00Z',
            updated_at: '2026-04-02T05:31:00Z',
          },
          latest_audio_job: {
            id: 'audio-job-2',
            status: 'in_progress',
            progress_percent: 64,
            current_step: 'Rendering segment 3 of 5',
            completed_segments: 3,
            total_segments: 5,
            current_segment_index: 3,
            attempt_count: 1,
            created_at: '2026-04-02T05:24:00Z',
            updated_at: '2026-04-02T05:31:00Z',
          },
        })}
      />,
    )

    expect(
      await screen.findByRole('heading', { name: 'Chapter 1' }),
    ).toBeInTheDocument()

    fireEvent.click(screen.getByRole('tab', { name: 'Listen back' }))

    expect(screen.getByText('Narration still rendering')).toBeInTheDocument()
    expect(
      screen.getAllByText('Rendering segment 3 of 5').length,
    ).toBeGreaterThan(0)
    expect(screen.getByText('64%')).toBeInTheDocument()
  })

  it('handles failed narration without losing the finish-line review surface', async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      new Response('# Chapter 1\n\nMira carried the lantern home.', {
        status: 200,
      }),
    )
    vi.stubGlobal('fetch', fetchMock)

    renderWithAppProviders(
      <FinalizeStage
        onAcceptRewrite={vi.fn().mockResolvedValue(undefined)}
        onDownloadAudio={vi.fn()}
        onDownloadStoryExport={vi.fn()}
        onKeepExploringRewrite={vi.fn()}
        onRejectRewrite={vi.fn().mockResolvedValue(undefined)}
        onRestoreSegmentVersion={vi.fn().mockResolvedValue(undefined)}
        onReturnToComposition={vi.fn()}
        snapshot={buildSnapshot({
          latest_composition_job: {
            ...baseSnapshot.latest_composition_job!,
            pending_review: false,
          },
          latest_story_asset: {
            id: 'story-asset-3',
            asset_kind: 'story_text',
            status: 'ready',
            access: {
              download_path:
                '/api/v1/sessions/session-finalize-1/assets/story-asset-3/content?disposition=attachment',
              filename: 'lanterns-over-juniper-lake.md',
              stream_path:
                '/api/v1/sessions/session-finalize-1/assets/story-asset-3/content?disposition=inline',
            },
            public_url:
              '/api/v1/sessions/session-finalize-1/assets/story-asset-3/content?disposition=inline',
            ready_at: '2026-04-02T05:28:00Z',
          },
          latest_audio_asset: null,
          latest_audio_job: {
            id: 'audio-job-3',
            status: 'failed',
            progress_percent: 77,
            current_step: 'Publishing compiled narration',
            error_message:
              'The worker could not merge the final narration master.',
            attempt_count: 2,
            created_at: '2026-04-02T05:24:00Z',
            updated_at: '2026-04-02T05:33:00Z',
          },
        })}
      />,
    )

    expect(
      await screen.findByRole('heading', { name: 'Chapter 1' }),
    ).toBeInTheDocument()

    fireEvent.click(screen.getByRole('tab', { name: 'Listen back' }))

    expect(
      screen.getByText(
        'Narration stopped before the final master was published',
      ),
    ).toBeInTheDocument()
    expect(
      screen.getAllByText(
        'The worker could not merge the final narration master.',
      ).length,
    ).toBeGreaterThan(0)
  })
})
