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
  it('renders the saved audio plan and estimate copy', () => {
    renderWithAppProviders(
      <AudioSettingsStage
        onSaveAudioSettings={vi.fn()}
        selectedStage={selectedStage}
        snapshot={sampleSnapshot}
      />,
    )

    expect(
      screen.getByText(
        'Shape the narration pass before the audio render starts.',
      ),
    ).toBeInTheDocument()
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

  it('renders active narration progress with the current durable step', () => {
    const snapshotWithActiveAudio: SessionSnapshot = {
      ...sampleSnapshot,
      active_audio_job: {
        id: 'audio-job-7',
        status: 'in_progress',
        progress_percent: 68,
        current_step: 'Mixing narration with the selected background bed.',
        current_step_index: 5,
        total_steps: 6,
        completed_segments: 3,
        total_segments: 3,
        current_segment_index: 3,
        estimated_duration_seconds: 780,
        updated_at: '2026-04-02T05:18:00Z',
      },
    }

    renderWithAppProviders(
      <AudioSettingsStage
        onSaveAudioSettings={vi.fn()}
        selectedStage={selectedStage}
        snapshot={snapshotWithActiveAudio}
      />,
    )

    expect(screen.getByText('68% rendered')).toBeInTheDocument()
    expect(
      screen.getByText('Mixing narration with the selected background bed.'),
    ).toBeInTheDocument()
    expect(
      screen.getAllByText(
        'Step 5 of 6. 3 of 3 narration segments are durable already. Estimated listening length 13 min.',
      ),
    ).toHaveLength(2)
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
