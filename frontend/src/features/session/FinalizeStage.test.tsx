import { fireEvent, screen, waitFor, within } from '@testing-library/react'
import {
  afterAll,
  afterEach,
  beforeAll,
  describe,
  expect,
  it,
  vi,
} from 'vitest'
import type {
  SessionArtifactInventoryItemView,
  SessionArtifactInventoryView,
  SessionSnapshot,
} from '../../api/sessions.ts'
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

function buildArtifactInventoryItem(
  key: SessionArtifactInventoryItemView['key'],
  overrides: Partial<SessionArtifactInventoryItemView> = {},
): SessionArtifactInventoryItemView {
  const baseByKey: Record<
    SessionArtifactInventoryItemView['key'],
    SessionArtifactInventoryItemView
  > = {
    story_text: {
      key: 'story_text',
      label: 'Final story text',
      artifact_kind: 'story_text',
      status: 'missing',
      status_detail: 'The accepted manuscript is not ready yet.',
      preview_assets: [],
      preview_asset_count: 0,
      download_path: null,
      stream_path: null,
    },
    story_docx: {
      key: 'story_docx',
      label: 'Word document',
      artifact_kind: 'story_docx',
      status: 'missing',
      status_detail: 'The Word export is not ready yet.',
      preview_assets: [],
      preview_asset_count: 0,
      download_path: null,
      stream_path: null,
    },
    final_audio: {
      key: 'final_audio',
      label: 'Final narration',
      artifact_kind: 'final_audio',
      status: 'missing',
      status_detail: 'The compiled narration master is not ready yet.',
      preview_assets: [],
      preview_asset_count: 0,
      download_path: null,
      stream_path: null,
    },
  }

  return {
    ...baseByKey[key],
    ...overrides,
    preview_assets: overrides.preview_assets ?? baseByKey[key].preview_assets,
  }
}

function buildArtifactInventory(
  items: SessionArtifactInventoryItemView[],
): SessionArtifactInventoryView {
  return {
    session_id: 'session-finalize-1',
    generated_at: '2026-04-02T05:35:00Z',
    items,
  }
}

function createFetchMock(options?: {
  inventory?: SessionArtifactInventoryView
  storyText?: string
  storyTextStatus?: number
}) {
  const inventory =
    options?.inventory ??
    buildArtifactInventory([
      buildArtifactInventoryItem('story_text'),
      buildArtifactInventoryItem('story_docx'),
      buildArtifactInventoryItem('final_audio'),
    ])
  const storyText =
    options?.storyText ?? '# Chapter 1\n\nMira carried the lantern home.'
  const storyTextStatus = options?.storyTextStatus ?? 200

  return vi.fn((input: RequestInfo | URL) => {
    const url = String(input)

    if (url.endsWith('/api/v1/sessions/session-finalize-1/artifacts')) {
      return Promise.resolve(
        new Response(JSON.stringify(inventory), {
          status: 200,
          headers: {
            'Content-Type': 'application/json',
          },
        }),
      )
    }

    if (
      url.includes('/assets/story-asset-') &&
      url.includes('disposition=inline')
    ) {
      return Promise.resolve(
        new Response(storyText, {
          status: storyTextStatus,
          headers: {
            'Content-Type': 'text/markdown; charset=utf-8',
          },
        }),
      )
    }

    return Promise.reject(new Error(`Unhandled fetch request: ${url}`))
  })
}

const originalScrollIntoView = HTMLElement.prototype.scrollIntoView
const scrollIntoViewMock = vi.fn()

beforeAll(() => {
  Object.defineProperty(HTMLElement.prototype, 'scrollIntoView', {
    configurable: true,
    value: scrollIntoViewMock,
  })
})

afterEach(() => {
  scrollIntoViewMock.mockReset()
  vi.restoreAllMocks()
  vi.unstubAllGlobals()
})

afterAll(() => {
  Object.defineProperty(HTMLElement.prototype, 'scrollIntoView', {
    configurable: true,
    value: originalScrollIntoView,
  })
})

describe('FinalizeStage', () => {
  it('keeps rewrite compare controls available from final review', async () => {
    vi.stubGlobal('fetch', createFetchMock())

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
        onReturnToAudioSettings={vi.fn()}
        onRestoreSegmentVersion={onRestoreSegmentVersion}
        onReturnToComposition={onReturnToComposition}
        onReturnToStorySetup={vi.fn()}
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
    const fetchMock = createFetchMock({
      inventory: buildArtifactInventory([
        buildArtifactInventoryItem('story_text', {
          status: 'ready',
          status_detail: 'The accepted manuscript is stored and ready.',
        }),
        buildArtifactInventoryItem('story_docx', {
          status: 'ready',
          status_detail: 'This Word export matches the latest manuscript.',
        }),
        buildArtifactInventoryItem('final_audio', {
          status: 'ready',
          status_detail: 'The compiled narration master is ready.',
        }),
      ]),
      storyText: `# Chapter 1: Lantern Wake

Mira carried the lantern home.

# Chapter 2: Moonlit Crossing

The harbor path glowed softly under the bridge.

# Chapter 3: Quiet Return

The oars slowed as the lake went still again.`,
    })
    vi.stubGlobal('fetch', fetchMock)

    const onDownloadAudio = vi.fn()
    const onDownloadStoryExport = vi.fn()
    const onReturnToAudioSettings = vi.fn()
    const onReturnToComposition = vi.fn()
    const onReturnToStorySetup = vi.fn()

    renderWithAppProviders(
      <FinalizeStage
        onAcceptRewrite={vi.fn().mockResolvedValue(undefined)}
        onDownloadAudio={onDownloadAudio}
        onDownloadStoryExport={onDownloadStoryExport}
        onKeepExploringRewrite={vi.fn()}
        onRejectRewrite={vi.fn().mockResolvedValue(undefined)}
        onReturnToAudioSettings={onReturnToAudioSettings}
        onRestoreSegmentVersion={vi.fn().mockResolvedValue(undefined)}
        onReturnToComposition={onReturnToComposition}
        onReturnToStorySetup={onReturnToStorySetup}
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
              segment_timeline: [
                {
                  segment_id: 'audio-segment-1',
                  segment_index: 1,
                  start_seconds: 0,
                  end_seconds: 210,
                  timeline_end_seconds: 213,
                  duration_seconds: 210,
                  pause_after_seconds: 3,
                  source_boundary_kind: 'chapter',
                  source_outline_card_key: 'chapter-1',
                  source_outline_card_title: 'Lantern Wake',
                },
                {
                  segment_id: 'audio-segment-2',
                  segment_index: 2,
                  start_seconds: 213,
                  end_seconds: 470,
                  timeline_end_seconds: 473,
                  duration_seconds: 257,
                  pause_after_seconds: 3,
                  source_boundary_kind: 'chapter',
                  source_outline_card_key: 'chapter-2',
                  source_outline_card_title: 'Moonlit Crossing',
                },
              ],
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
      await screen.findByRole('heading', { name: 'Chapter 1: Lantern Wake' }),
    ).toBeInTheDocument()
    expect(
      screen.getByRole('navigation', { name: 'Story contents' }),
    ).toBeInTheDocument()
    expect(
      screen.getByRole('button', { name: /Chapter 2: Moonlit Crossing/ }),
    ).toBeInTheDocument()
    expect(screen.getByText('Quest Fantasy')).toBeInTheDocument()
    expect(
      screen.getByText('1,800 words • ~12 min • 3 chapters'),
    ).toBeInTheDocument()

    fireEvent.click(
      screen.getByRole('button', { name: /Chapter 2: Moonlit Crossing/ }),
    )
    expect(scrollIntoViewMock).toHaveBeenCalledTimes(1)

    fireEvent.click(screen.getByRole('button', { name: 'Story setup' }))
    expect(onReturnToStorySetup).toHaveBeenCalledTimes(1)

    fireEvent.click(screen.getByRole('button', { name: 'Audio settings' }))
    expect(onReturnToAudioSettings).toHaveBeenCalledTimes(1)

    fireEvent.click(screen.getByRole('button', { name: 'Composition' }))
    expect(onReturnToComposition).toHaveBeenCalledTimes(1)

    fireEvent.click(
      await screen.findByRole('button', { name: 'Download Word document' }),
    )
    expect(onDownloadStoryExport).toHaveBeenCalledTimes(1)

    fireEvent.click(screen.getByRole('tab', { name: 'Listen back' }))
    expect(
      screen.getByRole('button', { name: 'Play narration' }),
    ).toBeInTheDocument()
    expect(screen.getByText('Text sync')).toBeInTheDocument()
    expect(
      screen.getByRole('button', { name: 'Open chapter in reader' }),
    ).toBeInTheDocument()

    fireEvent.click(
      await screen.findByRole('button', { name: 'Download narration' }),
    )
    expect(onDownloadAudio).toHaveBeenCalledTimes(1)
  })

  it('keeps the story readable while narration is still processing', async () => {
    const fetchMock = createFetchMock({
      inventory: buildArtifactInventory([
        buildArtifactInventoryItem('story_text', {
          status: 'ready',
          status_detail: 'The accepted manuscript is stored and ready.',
        }),
        buildArtifactInventoryItem('story_docx', {
          status: 'missing',
          status_detail: 'No Word export has been packaged yet.',
        }),
        buildArtifactInventoryItem('final_audio', {
          status: 'generating',
          status_detail:
            'Rendering segment 3 of 5. 1 preview clip is already available.',
          preview_asset_count: 1,
        }),
      ]),
    })
    vi.stubGlobal('fetch', fetchMock)

    renderWithAppProviders(
      <FinalizeStage
        onAcceptRewrite={vi.fn().mockResolvedValue(undefined)}
        onDownloadAudio={vi.fn()}
        onDownloadStoryExport={vi.fn()}
        onKeepExploringRewrite={vi.fn()}
        onRejectRewrite={vi.fn().mockResolvedValue(undefined)}
        onReturnToAudioSettings={vi.fn()}
        onRestoreSegmentVersion={vi.fn().mockResolvedValue(undefined)}
        onReturnToComposition={vi.fn()}
        onReturnToStorySetup={vi.fn()}
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

  it('builds reader navigation from accepted composition segments when the manuscript has no chapter headings', async () => {
    const fetchMock = createFetchMock({
      storyText: `Mira carried the lantern down to the harbor.

The bridge lights gathered under the oars.

The bell settled once the lake grew still.`,
    })
    vi.stubGlobal('fetch', fetchMock)

    renderWithAppProviders(
      <FinalizeStage
        onAcceptRewrite={vi.fn().mockResolvedValue(undefined)}
        onDownloadAudio={vi.fn()}
        onDownloadStoryExport={vi.fn()}
        onKeepExploringRewrite={vi.fn()}
        onRejectRewrite={vi.fn().mockResolvedValue(undefined)}
        onReturnToAudioSettings={vi.fn()}
        onRestoreSegmentVersion={vi.fn().mockResolvedValue(undefined)}
        onReturnToComposition={vi.fn()}
        onReturnToStorySetup={vi.fn()}
        snapshot={buildSnapshot({
          latest_composition_job: {
            ...baseSnapshot.latest_composition_job!,
            pending_review: false,
          },
          composition_segments: [
            {
              segment_index: 1,
              outline_card_title: 'Lantern wake',
              outline_card_summary: 'Mira leaves the harbor with the lantern.',
              current_version_id: 'segment-1-rev-1',
              current_revision_number: 1,
              is_stale: false,
              versions: [
                {
                  id: 'segment-1-rev-1',
                  composition_job_id: 'draft-job-1',
                  job_kind: 'draft',
                  segment_index: 1,
                  revision_number: 1,
                  status: 'completed',
                  acceptance_state: 'accepted',
                  is_current: true,
                  is_stale: false,
                  accepted_summary: 'The harbor remains calm as Mira leaves.',
                  text_content: 'Mira carried the lantern down to the harbor.',
                  word_count: 8,
                  created_at: '2026-04-02T05:10:00Z',
                  updated_at: '2026-04-02T05:12:00Z',
                  completed_at: '2026-04-02T05:12:00Z',
                },
              ],
            },
            {
              segment_index: 2,
              outline_card_title: 'Moonlit crossing',
              outline_card_summary: 'The bridge lights gather under the oars.',
              current_version_id: 'segment-2-rev-1',
              current_revision_number: 1,
              is_stale: false,
              versions: [
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
                  accepted_summary: 'The crossing stays gentle and luminous.',
                  text_content: 'The bridge lights gathered under the oars.',
                  word_count: 8,
                  created_at: '2026-04-02T05:12:00Z',
                  updated_at: '2026-04-02T05:14:00Z',
                  completed_at: '2026-04-02T05:14:00Z',
                },
              ],
            },
            {
              segment_index: 3,
              outline_card_title: 'Quiet return',
              outline_card_summary: 'The bell settles as the lake grows still.',
              current_version_id: 'segment-3-rev-1',
              current_revision_number: 1,
              is_stale: false,
              versions: [
                {
                  id: 'segment-3-rev-1',
                  composition_job_id: 'draft-job-1',
                  job_kind: 'draft',
                  segment_index: 3,
                  revision_number: 1,
                  status: 'completed',
                  acceptance_state: 'accepted',
                  is_current: true,
                  is_stale: false,
                  accepted_summary: 'The lake goes still again.',
                  text_content: 'The bell settled once the lake grew still.',
                  word_count: 8,
                  created_at: '2026-04-02T05:14:00Z',
                  updated_at: '2026-04-02T05:16:00Z',
                  completed_at: '2026-04-02T05:16:00Z',
                },
              ],
            },
          ],
          latest_story_asset: {
            id: 'story-asset-segment-navigation',
            asset_kind: 'story_text',
            status: 'ready',
            access: {
              download_path:
                '/api/v1/sessions/session-finalize-1/assets/story-asset-segment-navigation/content?disposition=attachment',
              filename: 'lanterns-over-juniper-lake.md',
              stream_path:
                '/api/v1/sessions/session-finalize-1/assets/story-asset-segment-navigation/content?disposition=inline',
            },
            public_url:
              '/api/v1/sessions/session-finalize-1/assets/story-asset-segment-navigation/content?disposition=inline',
            ready_at: '2026-04-02T05:28:00Z',
          },
        })}
      />,
    )

    expect(
      await screen.findAllByRole('heading', { name: 'Lantern wake' }),
    ).toHaveLength(2)
    const storyContents = screen.getByRole('navigation', {
      name: 'Story contents',
    })
    expect(
      within(storyContents).getByRole('button', { name: /Moonlit crossing/ }),
    ).toBeInTheDocument()
    expect(
      within(storyContents).getByRole('button', { name: /Quiet return/ }),
    ).toBeInTheDocument()
  })

  it('handles failed narration without losing the finish-line review surface', async () => {
    const fetchMock = createFetchMock({
      inventory: buildArtifactInventory([
        buildArtifactInventoryItem('story_text', {
          status: 'ready',
          status_detail: 'The accepted manuscript is stored and ready.',
        }),
        buildArtifactInventoryItem('story_docx', {
          status: 'missing',
          status_detail: 'No Word export has been packaged yet.',
        }),
        buildArtifactInventoryItem('final_audio', {
          status: 'failed',
          status_detail:
            'The worker could not merge the final narration master.',
        }),
      ]),
    })
    vi.stubGlobal('fetch', fetchMock)

    renderWithAppProviders(
      <FinalizeStage
        onAcceptRewrite={vi.fn().mockResolvedValue(undefined)}
        onDownloadAudio={vi.fn()}
        onDownloadStoryExport={vi.fn()}
        onKeepExploringRewrite={vi.fn()}
        onRejectRewrite={vi.fn().mockResolvedValue(undefined)}
        onReturnToAudioSettings={vi.fn()}
        onRestoreSegmentVersion={vi.fn().mockResolvedValue(undefined)}
        onReturnToComposition={vi.fn()}
        onReturnToStorySetup={vi.fn()}
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

  it('shows stale artifact messaging and actions in one inventory panel', async () => {
    const fetchMock = createFetchMock({
      inventory: buildArtifactInventory([
        buildArtifactInventoryItem('story_text', {
          status: 'ready',
          status_detail: 'The accepted manuscript is stored and ready.',
        }),
        buildArtifactInventoryItem('story_docx', {
          status: 'stale',
          status_detail:
            'The manuscript changed after the last Word export. Refresh it before sharing or downloading.',
        }),
        buildArtifactInventoryItem('final_audio', {
          status: 'stale',
          status_detail:
            'A newer narration pass is still running. The previous published master remains available in the meantime.',
        }),
      ]),
    })
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
        onReturnToAudioSettings={vi.fn()}
        onRestoreSegmentVersion={vi.fn().mockResolvedValue(undefined)}
        onReturnToComposition={vi.fn()}
        onReturnToStorySetup={vi.fn()}
        snapshot={buildSnapshot({
          latest_composition_job: {
            ...baseSnapshot.latest_composition_job!,
            pending_review: false,
          },
          latest_story_asset: {
            id: 'story-asset-4',
            asset_kind: 'story_text',
            status: 'ready',
            access: {
              download_path:
                '/api/v1/sessions/session-finalize-1/assets/story-asset-4/content?disposition=attachment',
              filename: 'lanterns-over-juniper-lake.md',
              stream_path:
                '/api/v1/sessions/session-finalize-1/assets/story-asset-4/content?disposition=inline',
            },
            public_url:
              '/api/v1/sessions/session-finalize-1/assets/story-asset-4/content?disposition=inline',
            ready_at: '2026-04-02T05:28:00Z',
          },
          latest_audio_asset: {
            id: 'audio-asset-4',
            asset_kind: 'final_audio',
            status: 'ready',
            access: {
              download_path:
                '/api/v1/sessions/session-finalize-1/assets/audio-asset-4/content?disposition=attachment',
              filename: 'lanterns-over-juniper-lake.wav',
              stream_path:
                '/api/v1/sessions/session-finalize-1/assets/audio-asset-4/content?disposition=inline',
            },
            public_url:
              '/api/v1/sessions/session-finalize-1/assets/audio-asset-4/content?disposition=inline',
            audio_job_id: 'audio-job-old',
            ready_at: '2026-04-02T05:20:00Z',
          },
          active_audio_job: {
            id: 'audio-job-new',
            status: 'in_progress',
            progress_percent: 72,
            current_step: 'Mixing a replacement narration master',
            completed_segments: 5,
            total_segments: 5,
            current_segment_index: 5,
            attempt_count: 1,
            created_at: '2026-04-02T05:24:00Z',
            updated_at: '2026-04-02T05:31:00Z',
          },
          latest_audio_job: {
            id: 'audio-job-new',
            status: 'in_progress',
            progress_percent: 72,
            current_step: 'Mixing a replacement narration master',
            completed_segments: 5,
            total_segments: 5,
            current_segment_index: 5,
            attempt_count: 1,
            created_at: '2026-04-02T05:24:00Z',
            updated_at: '2026-04-02T05:31:00Z',
          },
        })}
      />,
    )

    expect(
      await screen.findByRole('button', { name: 'Refresh Word document' }),
    ).toBeInTheDocument()
    expect(
      screen.getByRole('button', { name: 'Download previous master' }),
    ).toBeInTheDocument()
    expect(screen.getAllByText('Stale').length).toBeGreaterThanOrEqual(2)

    fireEvent.click(
      screen.getByRole('button', { name: 'Refresh Word document' }),
    )
    expect(onDownloadStoryExport).toHaveBeenCalledTimes(1)

    fireEvent.click(
      screen.getByRole('button', { name: 'Download previous master' }),
    )
    expect(onDownloadAudio).toHaveBeenCalledTimes(1)
  })
})
