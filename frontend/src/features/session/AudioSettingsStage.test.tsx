import { fireEvent, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import type { SessionSnapshot } from '../../api/sessions.ts'
import { renderWithAppProviders } from '../../test/renderWithAppProviders.tsx'
import type { SessionWorkspaceStageView } from './sessionStageScaffold.ts'
import { AudioSettingsStage } from './AudioSettingsStage.tsx'

const sampleSnapshot: SessionSnapshot = {
  id: 'moonlit-harbor',
  display_title: 'Lanterns Over Juniper Lake',
  current_stage: 'audio',
  resume_stage: 'audio',
  furthest_completed_stage: 'composition',
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
    completed_stages: 8,
    in_progress_stages: 1,
    needs_regeneration_stages: 0,
  },
  stage_states: [
    {
      stage: 'audio',
      label: 'Audio',
      description:
        'Configure narration settings and generate resumable audio artifacts.',
      status: 'in_progress',
      detail: 'Tune narration settings.',
    },
  ],
  latest_story_asset: {
    id: 'story-asset-1',
    asset_kind: 'story_text',
    status: 'ready',
    ready_at: '2026-04-02T05:10:00Z',
  },
  latest_audio_asset: null,
  audio_settings: {
    voice_key: 'moonbeam',
    narration_style: 'calm',
    playback_speed: 0.95,
    include_background_music: false,
    music_profile: 'lullaby_piano',
    narration_volume: 92,
    music_volume: 24,
    guidance_notes: null,
    runtime_estimate: {
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
    },
  },
}

const selectedStage: SessionWorkspaceStageView = {
  stage: 'audio',
  label: 'Audio',
  description:
    'Configure narration settings and generate resumable audio artifacts.',
  status: 'in_progress',
  detail: 'Tune narration settings.',
  availability: 'unlocked',
  index: 8,
  invalidatesOnEdit: ['finalize'],
  isCurrent: true,
  isSelected: true,
  scaffoldBullets: [],
  scaffoldSummary: 'Audio settings live here.',
  scaffoldTitle: 'Audio',
}

describe('AudioSettingsStage', () => {
  it('renders the saved audio plan, progress surface, and estimate copy', () => {
    renderWithAppProviders(
      <AudioSettingsStage
        onSaveAudioSettings={vi.fn()}
        selectedStage={selectedStage}
        snapshot={sampleSnapshot}
      />,
    )

    expect(
      screen.getByText(
        'Narration progress will appear here once audio generation starts.',
      ),
    ).toBeInTheDocument()
    expect(screen.getByText('Segment status')).toBeInTheDocument()
    expect(screen.getByText('Approx. 14 min')).toBeInTheDocument()
    expect(
      screen.getByText(
        'Usually 12-16 min. Approximate preview based on story setup target.',
      ),
    ).toBeInTheDocument()
    expect(screen.getByLabelText('Narration voice')).toHaveValue('moonbeam')
    expect(screen.getByLabelText('Narration style')).toHaveValue('calm')
  })

  it('updates the approximate estimate immediately when playback speed changes', () => {
    renderWithAppProviders(
      <AudioSettingsStage
        onSaveAudioSettings={vi.fn()}
        selectedStage={selectedStage}
        snapshot={sampleSnapshot}
      />,
    )

    fireEvent.change(screen.getByLabelText('Playback speed'), {
      target: { value: '0.85' },
    })

    expect(screen.getByText('Approx. 15 min')).toBeInTheDocument()
    expect(
      screen.getByText(
        'Usually 13-18 min. Approximate preview based on story setup target.',
      ),
    ).toBeInTheDocument()
    expect(
      screen.getByText(
        /Assumes about 140 words per minute at 0.85x, usually 120-160 words per minute, plus 2 short chapter pauses at roughly 3 seconds each\./,
      ),
    ).toBeInTheDocument()
  })

  it('saves the full audio settings form state through the workspace callback', async () => {
    const onSaveAudioSettings = vi.fn().mockResolvedValue({
      event: {
        id: 'audio-event-1',
        session_id: 'moonlit-harbor',
        sequence_number: 1,
        actor: { actor_type: 'user' },
        event_type: 'content.user_edit.recorded',
        stage: 'audio',
        summary: 'Saved user edit for audio settings.',
        payload: null,
        created_at: '2026-04-02T05:20:00Z',
      },
      snapshot: sampleSnapshot,
    })

    renderWithAppProviders(
      <AudioSettingsStage
        onSaveAudioSettings={onSaveAudioSettings}
        selectedStage={selectedStage}
        snapshot={sampleSnapshot}
      />,
    )

    fireEvent.change(screen.getByLabelText('Narration voice'), {
      target: { value: 'storykeeper' },
    })
    fireEvent.change(screen.getByLabelText('Playback speed'), {
      target: { value: '1.05' },
    })
    fireEvent.click(screen.getByLabelText('Background music'))
    fireEvent.change(screen.getByLabelText('Music style'), {
      target: { value: 'night_ambience' },
    })
    fireEvent.change(screen.getByLabelText('Narration volume'), {
      target: { value: '89' },
    })
    fireEvent.change(screen.getByLabelText('Music volume'), {
      target: { value: '15' },
    })
    fireEvent.change(screen.getByLabelText('Mix and delivery note'), {
      target: { value: 'Lean even softer on chapter endings.' },
    })
    fireEvent.click(screen.getByRole('button', { name: 'Save audio settings' }))

    expect(onSaveAudioSettings).toHaveBeenCalledWith({
      voiceKey: 'storykeeper',
      narrationStyle: 'calm',
      playbackSpeed: 1.05,
      includeBackgroundMusic: true,
      musicProfile: 'night_ambience',
      narrationVolume: 89,
      musicVolume: 15,
      guidanceNotes: 'Lean even softer on chapter endings.',
      origin: 'workspace',
    })
  })

  it('renders active narration progress with segment previews and a distinct final master player', () => {
    const snapshotWithActiveAudio: SessionSnapshot = {
      ...sampleSnapshot,
      active_audio_job: {
        id: 'audio-job-7',
        status: 'in_progress',
        progress_percent: 68,
        current_step: 'Rendering narration segment 2 of 3.',
        current_step_index: 2,
        total_steps: 6,
        completed_segments: 1,
        total_segments: 3,
        current_segment_index: 2,
        estimated_duration_seconds: 780,
        updated_at: '2026-04-02T05:18:00Z',
      },
      latest_audio_job: {
        id: 'audio-job-7',
        status: 'in_progress',
        progress_percent: 68,
        current_step: 'Rendering narration segment 2 of 3.',
        current_step_index: 2,
        total_steps: 6,
        completed_segments: 1,
        total_segments: 3,
        current_segment_index: 2,
        estimated_duration_seconds: 780,
        updated_at: '2026-04-02T05:18:00Z',
      },
      audio_segments: [
        {
          id: 'segment-1',
          audio_job_id: 'audio-job-7',
          segment_index: 1,
          status: 'completed',
          source_boundary_kind: 'chapter',
          source_outline_card_title: 'Lantern launch',
          word_count: 212,
          pause_after_seconds: 3,
          pause_hint: 'chapter_break',
          split_reason: 'paragraph_boundary',
          text_preview:
            'Mira set the first lantern down on the still water and waited for the harbor to answer in a hush.',
          preview_asset: {
            id: 'preview-1',
            asset_kind: 'audio_segment',
            status: 'ready',
            public_url: 'http://localhost:8568/storage/v1/b/storyteller-audio/o/sessions/moonlit-harbor/audio/jobs/audio-job-7/segments/0001.wav?alt=media',
          },
        },
        {
          id: 'segment-2',
          audio_job_id: 'audio-job-7',
          segment_index: 2,
          status: 'queued',
          source_boundary_kind: 'chapter',
          source_outline_card_title: 'Silver bell crossing',
          word_count: 248,
          pause_after_seconds: 0,
          pause_hint: 'none',
          split_reason: 'sentence_boundary',
          text_preview:
            'Otis stayed close while the silver bell called from the cove, never letting the mystery sharpen.',
        },
        {
          id: 'segment-3',
          audio_job_id: 'audio-job-7',
          segment_index: 3,
          status: 'queued',
          source_boundary_kind: 'chapter',
          source_outline_card_title: 'Harbor homecoming',
          word_count: 231,
          pause_after_seconds: 0,
          pause_hint: 'none',
          split_reason: 'paragraph_boundary',
        },
      ],
      latest_audio_asset: {
        id: 'final-audio',
        asset_kind: 'final_audio',
        status: 'ready',
        audio_job_id: 'audio-job-6',
        duration_seconds: 812,
        details: {
          generation: {
            voice_key: 'moonbeam',
          },
          mix: {
            applied: false,
          },
        },
        public_url: 'http://localhost:8568/storage/v1/b/storyteller-audio/o/sessions/moonlit-harbor/audio/jobs/audio-job-6/final/story.wav?alt=media',
        ready_at: '2026-04-02T05:22:00Z',
      },
    }

    renderWithAppProviders(
      <AudioSettingsStage
        onSaveAudioSettings={vi.fn()}
        selectedStage={selectedStage}
        snapshot={snapshotWithActiveAudio}
      />,
    )

    expect(screen.getByText('68%')).toBeInTheDocument()
    expect(screen.getAllByText('Generating').length).toBeGreaterThan(0)
    expect(screen.getByText('Ready for preview')).toBeInTheDocument()
    expect(screen.getByText('Generating now')).toBeInTheDocument()
    expect(screen.getByText('Compiled narration')).toBeInTheDocument()
    expect(screen.getByText('Checkpoint preview clip')).toBeInTheDocument()
    expect(screen.getByText('Final audio')).toBeInTheDocument()
    expect(
      screen.getByLabelText('Segment 1 preview audio'),
    ).toBeInTheDocument()
    expect(
      screen.getByLabelText('Compiled narration preview'),
    ).toBeInTheDocument()
    expect(
      screen.getByText(
        /This player is showing the previous published master while the current narration run assembles a replacement\./,
      ),
    ).toBeInTheDocument()
    expect(screen.getByText('Runtime 13m 32s')).toBeInTheDocument()
    expect(screen.getByText('Voice moonbeam')).toBeInTheDocument()
    expect(screen.getByText('Voice only')).toBeInTheDocument()
    expect(
      screen.getByRole('link', { name: 'Download narration' }),
    ).toBeInTheDocument()
  })

  it('renders backend-provided music catalog guidance when music is enabled', () => {
    const snapshotWithMusic: SessionSnapshot = {
      ...sampleSnapshot,
      audio_settings: {
        ...sampleSnapshot.audio_settings!,
        include_background_music: true,
        music_profile: 'night_ambience',
        music_profile_options: [
          {
            key: 'night_ambience',
            label: 'Night ambience',
            description:
              'Low environmental bed for harbor, forest, or sky scenes.',
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
        ],
        mix_preview: {
          strategy: 'curated_bed_ducked',
          summary:
            'Night ambience loops under the narration at -30.9 dB before ducking. Voice gain -1.1 dB, 8:1 ducking, and an 8s fade out.',
          track_key: 'night_ambience',
          track_label: 'Night ambience',
          track_description:
            'Low environmental bed for harbor, forest, or sky scenes.',
          narration_gain_db: -1.1,
          music_gain_db: -30.9,
          ducking_ratio: 8,
          ducking_threshold: 0.05,
          fade_out_seconds: 8,
          loop_duration_seconds: 24,
        },
      },
    }

    renderWithAppProviders(
      <AudioSettingsStage
        onSaveAudioSettings={vi.fn()}
        selectedStage={selectedStage}
        snapshot={snapshotWithMusic}
      />,
    )

    expect(
      screen.getByText(
        'Fits scene-setting passages that want a steady sense of place.',
      ),
    ).toBeInTheDocument()
    expect(
      screen.getByText(
        /Night ambience loops under the narration at -30.9 dB before ducking\./,
      ),
    ).toBeInTheDocument()
  })
})
